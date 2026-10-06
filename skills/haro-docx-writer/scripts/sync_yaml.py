#!/usr/bin/env python3
"""Sync a haro-docx-writer template.yaml FROM its template.docx (.docx wins).

Overwrites only the styles/page blocks (+ _extracted facts, content.txt,
logo re-extract). Identity params, meta, cover/header_footer/toc_levels are
YAML-owned and left untouched. No backup is made (per design decision).

Usage:
    python sync_yaml.py --id <template-id> [--project-root .]

Exit codes: 0 = synced (even with zero changes), 2 = error.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_template import (  # noqa: E402
    _header_image_blobs,
    dump_content,
    extract_visual,
    merge_visual_into_cfg,
    save_logo_blob,
)
from template_store import normalize_id, now_iso, resolve  # noqa: E402


def _flat(prefix: str, mapping: dict) -> dict:
    return {f"{prefix}.{k}": v for k, v in (mapping or {}).items()}


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="haro-docx-writer yaml sync (docx wins)")
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
    if not hit or not hit["yaml"].exists():
        print(
            f"LỖI: không tìm thấy mẫu '{tid}'. Chạy /haro-docx-writer --list để xem danh sách.",
            file=sys.stderr,
        )
        return 2
    if not hit["docx"].exists():
        print(f"LỖI: thiếu file mẫu ({hit['docx']}).", file=sys.stderr)
        return 2
    with open(hit["yaml"], encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    before = {**_flat("styles", cfg.get("styles")), **_flat("page", cfg.get("page"))}
    try:
        doc = Document(str(hit["docx"]))
        visual = extract_visual(hit["docx"])
        logo_rel = save_logo_blob(_header_image_blobs(doc), hit["dir"])
    except Exception as e:
        print(f"LỖI: không đọc được file mẫu ({e}).", file=sys.stderr)
        return 2

    merge_visual_into_cfg(cfg, visual)
    ext = cfg.get("_extracted", {}) or {}
    ext.update(
        {
            "has_header": visual.get("has_header", False),
            "header_text": visual.get("header_text", ""),
            "header_has_image": visual.get("header_has_image", False),
            "has_footer": visual.get("has_footer", False),
            "footer_text": visual.get("footer_text", ""),
            "has_code_style": visual.get("has_code_style", False),
        }
    )
    if logo_rel:
        ext["logo_saved"] = logo_rel
    cfg["_extracted"] = ext
    cfg["updated_at"] = now_iso()
    with open(hit["yaml"], "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
    with open(hit["dir"] / "content.txt", "w", encoding="utf-8") as f:
        f.write(dump_content(doc, hit["docx"].name, ext.get("logo_saved", "")))

    after = {**_flat("styles", cfg.get("styles")), **_flat("page", cfg.get("page"))}
    diffs = [
        f"{k}: '{before.get(k)}' -> '{after.get(k)}'"
        for k in sorted(set(before) | set(after))
        if before.get(k) != after.get(k)
    ]
    print(f"Đã đồng bộ YAML từ .docx cho mẫu '{tid}' ({hit['location']}, không backup).")
    if diffs:
        print("docx thắng ở các mục:")
        for d in diffs:
            print(f"  - {d}")
    else:
        print("Không có gì thay đổi — YAML đã khớp .docx.")
    if logo_rel:
        print(f"Logo bóc lại: {logo_rel}")
    print(f"YAML: {hit['yaml']}")
    print(f"Kiểm tra: /haro-docx-writer --validate:{tid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
