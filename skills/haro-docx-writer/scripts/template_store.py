#!/usr/bin/env python3
"""Shared registry helpers for haro-docx-writer templates (local + global).

Layout:
    <project>/.haro-docx-writer/templates/<id>/template.docx + template.yaml
    ~/.haro-docx-writer/templates/<id>/template.docx + template.yaml

Resolution order: local wins over global when both exist.

Language convention: code/comments in English; user-visible strings in
Vietnamese with full diacritics.
"""
from __future__ import annotations

import datetime
import re
import shutil
import sys
from pathlib import Path

import yaml

TEMPLATE_DOCX_NAME = "template.docx"
TEMPLATE_YAML_NAME = "template.yaml"

ID_RE = re.compile(r"^[a-z0-9][a-z0-9\-_]{0,40}$")
MAX_ID_LEN = 41


def normalize_id(raw: str) -> str:
    tid = (raw or "").strip().lower().replace(" ", "-")
    if not tid:
        raise ValueError("LỖI: id mẫu rỗng. Ví dụ: /haro-docx-writer --create:congty-a <file.docx>")
    if len(tid) > MAX_ID_LEN or not ID_RE.match(tid):
        raise ValueError(
            f"LỖI: id '{raw}' không hợp lệ. Id gồm 2–41 ký tự: chữ thường, số, '-' hoặc '_'."
        )
    return tid


def local_root(project_root: Path) -> Path:
    return Path(project_root).resolve() / ".haro-docx-writer" / "templates"


def global_root() -> Path:
    return Path.home() / ".haro-docx-writer" / "templates"


def template_paths(root: Path, tid: str) -> dict:
    d = Path(root) / tid
    return {
        "dir": d,
        "docx": d / TEMPLATE_DOCX_NAME,
        "yaml": d / TEMPLATE_YAML_NAME,
    }


def exists_in(root: Path, tid: str) -> bool:
    p = template_paths(root, tid)
    return p["yaml"].exists() or p["docx"].exists()


def resolve(tid: str, project_root: Path) -> dict | None:
    """Return the winning entry for tid (local first, then global), or None."""
    tid = normalize_id(tid)
    lr = local_root(project_root)
    if exists_in(lr, tid):
        p = template_paths(lr, tid)
        return {"id": tid, "location": "local", "root": lr, **p}
    gr = global_root()
    if exists_in(gr, tid):
        p = template_paths(gr, tid)
        return {"id": tid, "location": "global", "root": gr, **p}
    return None


def resolve_all(tid: str, project_root: Path) -> list[dict]:
    """Return every scope holding tid (for duplicate warnings)."""
    tid = normalize_id(tid)
    out = []
    for loc, root in (("local", local_root(project_root)), ("global", global_root())):
        if exists_in(root, tid):
            p = template_paths(root, tid)
            out.append({"id": tid, "location": loc, "root": root, **p})
    return out


def read_meta(yaml_path: Path) -> dict:
    try:
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def list_all(project_root: Path) -> list[dict]:
    """Scan local + global registries. Sorted by id, local first on ties."""
    rows: list[dict] = []
    for loc, root in (("local", local_root(project_root)), ("global", global_root())):
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            yml = child / TEMPLATE_YAML_NAME
            meta = read_meta(yml) if yml.exists() else {}
            rows.append(
                {
                    "id": meta.get("id", child.name),
                    "name": meta.get("name", "(Chưa đặt tên)"),
                    "description": meta.get("description", ""),
                    "location": loc,
                    "created_at": meta.get("created_at", ""),
                    "updated_at": meta.get("updated_at", ""),
                    "dir": child,
                    "docx": child / TEMPLATE_DOCX_NAME,
                    "yaml": yml,
                }
            )
    rows.sort(key=lambda r: (r["id"], 0 if r["location"] == "local" else 1))
    return rows


def now_iso() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_source_into(source: Path, dest_docx: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"LỖI: không tìm thấy file '{source}'.")
    if source.suffix.lower() != ".docx":
        raise ValueError(
            f"LỖI: file tạo mẫu phải là .docx (nhận được '{source.suffix or '(không đuôi)'}')."
        )
    ensure_parent(dest_docx)
    shutil.copy2(str(source), str(dest_docx))


def delete_template(tid: str, location: str, project_root: Path) -> Path:
    tid = normalize_id(tid)
    root = local_root(project_root) if location == "local" else global_root()
    target = root / tid
    if not target.exists():
        raise FileNotFoundError(
            f"LỖI: không tìm thấy mẫu '{tid}' ở {location} ({target})."
        )
    shutil.rmtree(str(target))
    return target


def _print_rows(rows: list[dict]) -> None:
    if not rows:
        print("Chưa có mẫu nào. Tạo mẫu mới: /haro-docx-writer --create:<id> <file.docx>")
        return
    header = f"{'id':<20} {'tên mẫu':<30} {'vị trí':<7} {'tạo lúc':<25} {'cập nhật lúc':<25}  mô tả"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r['id']:<20} {str(r['name'])[:30]:<30} {r['location']:<7} "
            f"{str(r['created_at'])[:25]:<25} {str(r['updated_at'])[:25]:<25}  {r['description']}"
        )


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass
    import argparse

    ap = argparse.ArgumentParser(description="haro-docx-writer template registry helper")
    ap.add_argument("--project-root", default=".", help="project root (for local scope)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list local + global templates")
    p_get = sub.add_parser("resolve", help="print resolved paths for an id")
    p_get.add_argument("id")
    args = ap.parse_args(argv)
    project_root = Path(args.project_root)
    if args.cmd == "list":
        _print_rows(list_all(project_root))
        return 0
    if args.cmd == "resolve":
        hit = resolve(args.id, project_root)
        if not hit:
            print(f"LỖI: không tìm thấy mẫu '{args.id}'.", file=sys.stderr)
            return 2
        print(f"id:       {hit['id']}")
        print(f"vị trí:    {hit['location']}")
        print(f"thư mục:  {hit['dir']}")
        print(f"file yaml: {hit['yaml']}")
        print(f"file mẫu:  {hit['docx']}")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
