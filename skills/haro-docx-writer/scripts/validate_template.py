#!/usr/bin/env python3
"""Validate that a haro-docx-writer template.yaml matches its template.docx.

Style-level only (per user decision): compare YAML `styles/*` against the
actual .docx styles, plus header/footer presence recorded in `_extracted`,
plus logo file existence. Run-level oddities are ignored to avoid false
positives.

Usage:
    python validate_template.py --id <template-id> [--project-root .]

Exit codes: 0 = all match, 1 = mismatches found, 2 = error.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_template import extract_visual  # noqa: E402
from template_store import normalize_id, parse_cm, parse_pt, resolve  # noqa: E402


def _eq_font(a: str, b: str) -> bool:
    return (a or "").strip().lower() == (b or "").strip().lower()


def _eq_size(a, b) -> bool:
    try:
        return abs(float(a) - float(b)) < 0.05
    except (TypeError, ValueError):
        return (a or "") == (b or "")


def _eq_len(key: str, a, b) -> bool:
    """Compare numerics after normalizing units (cm-keys vs pt-keys).

    Bare numbers keep legacy meaning (key's own unit); suffixed strings
    convert. Tolerance 0.05 in the canonical unit.
    """
    parse = parse_cm if key.endswith("_cm") else parse_pt
    try:
        return abs(parse(a, "yaml") - parse(b, "docx")) < 0.05
    except (TypeError, ValueError):
        return (a or "") == (b or "")


def _eq_num(key: str):
    return lambda y, d: _eq_len(key, y, d)


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="haro-docx-writer template validator")
    ap.add_argument("--id", required=True, help="id mau")
    ap.add_argument("--project-root", default=".")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass
    args = parse_args(argv)
    try:
        tid = normalize_id(args.id)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    hit = resolve(tid, Path(args.project_root))
    if not hit:
        print(
            f"LỖI: không tìm thấy mẫu '{tid}'. Chạy /haro-docx-writer --list để xem danh sách.",
            file=sys.stderr,
        )
        return 2
    if not hit["yaml"].exists():
        print(f"LỖI: thiếu file YAML ({hit['yaml']}).", file=sys.stderr)
        return 2
    if not hit["docx"].exists():
        print(f"LỖI: thiếu file mẫu ({hit['docx']}).", file=sys.stderr)
        return 2
    with open(hit["yaml"], encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    styles = cfg.get("styles", {}) or {}
    recorded = cfg.get("_extracted", {}) or {}
    try:
        visual = extract_visual(hit["docx"])
    except Exception as e:
        print(f"LỖI: không đọc được file mẫu ({e}).", file=sys.stderr)
        return 2

    rows: list[tuple[str, str, str, bool]] = []

    def add(label: str, yaml_val, docx_val, ok: bool):
        rows.append((label, str(yaml_val), str(docx_val), ok))

    def add_cmp(label: str, yaml_val, docx_val, cmp) -> None:
        """Compare only what EXISTS in the .docx.

        A missing docx attribute (inherited theme default, never set) never
        conflicts with the yaml — at render the yaml wins. Only two explicit,
        differing values count as LỆCH.
        """
        if docx_val is None or (isinstance(docx_val, str) and docx_val == ""):
            rows.append((label, str(yaml_val), "(dùng YAML)", True))
        else:
            add(label, yaml_val, docx_val, cmp(yaml_val, docx_val))

    add_cmp("styles.body_font", styles.get("body_font", ""),
            visual.get("body_font", ""), _eq_font)
    for key in ("body_size", "body_line_spacing", "body_space_before", "body_space_after",
                "h1_size", "h2_size", "h3_size", "h4_size", "h5_size", "h6_size",
                "heading_space_before", "heading_space_after",
                "bullet_indent_cm", "bullet_space_after"):
        yv = styles.get(key, "")
        dv = visual.get(key, "")
        if yv == "" and (dv == "" or dv is None):
            continue
        add_cmp(f"styles.{key}", yv, dv, _eq_num(key))
    if visual.get("has_code_style", True):
        add_cmp("styles.code_font", styles.get("code_font", ""),
                visual.get("code_font", ""), _eq_font)
        if styles.get("code_size") or visual.get("code_size"):
            add_cmp("styles.code_size", styles.get("code_size", ""),
                    visual.get("code_size", ""), _eq_num("code_size"))

    page = cfg.get("page", {}) or {}
    if page or visual.get("page_size"):
        add_cmp("page.size", page.get("size", ""), visual.get("page_size", ""),
                lambda y, d: str(y).upper() == str(d).upper() or not y or not d)
        add_cmp("page.orientation", page.get("orientation", ""), visual.get("page_orientation", ""),
                lambda y, d: str(y).lower() == str(d).lower() or not y or not d)
        margins = visual.get("page_margins_cm") or {}
        for side, pkey in (("top", "margin_top_cm"), ("bottom", "margin_bottom_cm"),
                           ("left", "margin_left_cm"), ("right", "margin_right_cm")):
            yv = page.get(pkey, "")
            dv = margins.get(side, "")
            if yv == "" and (dv == "" or dv is None):
                continue
            add_cmp(f"page.{pkey}", yv, dv, _eq_num(pkey))
        for label, pkey, vkey in (("header_distance", "header_distance_cm", "page_header_distance_cm"),
                                  ("footer_distance", "footer_distance_cm", "page_footer_distance_cm")):
            yv = page.get(pkey, "")
            dv = visual.get(vkey, "")
            if yv == "" and (dv == "" or dv is None):
                continue
            add_cmp(f"page.{pkey}", yv, dv, _eq_num(pkey))

    if recorded:
        add("header (có/không)", "có" if recorded.get("has_header") else "không có",
            "có" if visual.get("has_header") else "không có",
            bool(recorded.get("has_header")) == bool(visual.get("has_header")))
        add("footer (có/không)", "có" if recorded.get("has_footer") else "không có",
            "có" if visual.get("has_footer") else "không có",
            bool(recorded.get("has_footer")) == bool(visual.get("has_footer")))
        add("logo trong header", "có" if recorded.get("header_has_image") else "không có",
            "có" if visual.get("header_has_image") else "không có",
            bool(recorded.get("header_has_image")) == bool(visual.get("header_has_image")))

    logo = ((cfg.get("header") or {}).get("logo_path") or "").strip()
    if logo:
        base = hit["yaml"].parent
        lp = Path(logo) if Path(logo).is_absolute() else (base / logo)
        if not lp.exists():
            # project-root relative fallback
            alt = Path(args.project_root) / logo
            ok = alt.exists()
            rows.append(("header.logo_path (file tồn tại)", logo, "không tìm thấy", ok))
        else:
            rows.append(("header.logo_path (file tồn tại)", logo, "tồn tại", True))

    print(f"Kết quả kiểm tra mẫu '{tid}' ({hit['location']}):")
    print(f"  YAML: {hit['yaml']}")
    print(f"  DOCX: {hit['docx']}")
    bad = 0
    for label, yv, dv, ok in rows:
        mark = "KHỚP" if ok else "LỆCH"
        if not ok:
            bad += 1
        print(f"  [{mark}] {label}: yaml='{yv}' | docx='{dv}'")
    if bad:
        print(f"Có {bad} mục LỆCH. Cách sửa:")
        print(f"  - Nếu vừa sửa file .docx: cập nhật YAML cho khớp (hoặc chạy lại trích xuất rồi sửa tay).")
        print(f"  - Nếu vừa sửa YAML: chạy /haro-docx-writer --update:{tid} <nội dung> để đẩy style vào file mẫu.")
        return 1
    print("Tất cả khớp. Mẫu sẵn sàng để xuất.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
