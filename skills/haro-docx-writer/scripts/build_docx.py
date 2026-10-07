#!/usr/bin/env python3
"""Render user content (markdown/text/pdf) into a template's .docx.

The template governs pages, styles, and chrome — this script only renders
fresh body content into it (stripping the template's sample body first),
fills {{name}}/[[name]] placeholders, and applies the yaml page block.
Implements skills/haro-docx-writer/shared/docx-style.md. This is the ONLY
supported way to produce .docx in haro-docx-writer — agents must call this
script, never hand-craft documents.
Requires: python-docx, pyyaml. Optional: pypdf (only for .pdf input).

Usage:
    python build_docx.py --input <file.md|txt|pdf> --output <out.docx>
                         [--config <template.yaml>] [--base-template <tpl.docx>]
                         [--template-id <id> --project-root .] [--param k=v ...]
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from template_store import resolve as resolve_template
except ImportError:  # script copied standalone
    resolve_template = None  # type: ignore


def parse_pt(value, field="giá trị"):
    """Parse to points; single definition (no union) for strict checkers."""
    try:
        from template_store import parse_pt as _impl
    except ImportError:  # standalone copy — legacy plain-number behavior
        return float(value)
    return _impl(value, field)


def parse_cm(value, field="giá trị"):
    """Parse to centimeters; single definition (no union) for strict checkers."""
    try:
        from template_store import parse_cm as _impl
    except ImportError:  # standalone copy — legacy plain-number behavior
        return float(value)
    return _impl(value, field)


def _num(mapping: dict, key: str, default, unit: str, prefix: str):
    """Read a numeric param through the unit parser; exit cleanly on bad input.

    Takes a unit tag instead of a callable so strict checkers never see a
    function passed as a value.
    """
    try:
        if unit == "cm":
            return parse_cm(mapping.get(key, default), f"{prefix}.{key}")
        return parse_pt(mapping.get(key, default), f"{prefix}.{key}")
    except ValueError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(2)


def _cfg_pt(mapping: dict, key: str, default, prefix: str = "styles"):
    return Pt(_num(mapping, key, default, "pt", prefix))


def _cfg_cm(mapping: dict, key: str, default, prefix: str = "styles"):
    return Cm(_num(mapping, key, default, "cm", prefix))


def _cfg_float(mapping: dict, key: str, default, prefix: str = "styles") -> float:
    try:
        return float(str(mapping.get(key, default)).strip())
    except (TypeError, ValueError):
        print(f"LỖI: '{prefix}.{key}' phải là số (nhận được '{mapping.get(key)}').",
              file=sys.stderr)
        raise SystemExit(2)

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

HYPERLINK_BLUE = RGBColor(0x05, 0x63, 0xC1)
QUOTE_FALLBACK_INDENT = Cm(1.0)

# ---------------------------------------------------------------- config

DEFAULTS = {
    "company_name": "(Chưa xác định)",
    "solution_name": "(Chưa xác định)",
    "document_name": "(Chưa xác định)",
    "document_title": "(Chưa xác định)",
    "version": "1.0",
    "date": datetime.date.today().strftime("%d/%m/%Y"),
    "status": "Ban hành",
    "authors": [],
    "reviewers": [],
    "approvers": [],
    "styles": {
        "body_font": "Times New Roman",
        "code_font": "Consolas",
        "body_size": 12,
        "h1_size": 14,
        "h2_size": 13,
        "h3_size": 12,
        "h4_size": 12,
        "h5_size": 11,
        "h6_size": 11,
        "body_line_spacing": 1.15,
        "body_space_before": 0,
        "body_space_after": 6,
        "heading_space_before": 12,
        "heading_space_after": 6,
        "bullet_indent_cm": 0.75,
        "bullet_space_after": 2,
        "code_size": 11,
    },
    "page": {
        "size": "A4",
        "orientation": "portrait",
        "margin_top_cm": 2.54,
        "margin_bottom_cm": 2.54,
        "margin_left_cm": 2.0,
        "margin_right_cm": 2.0,
        "header_distance_cm": 1.27,
        "footer_distance_cm": 1.27,
    },
    "figure_caption": "Figure {n}: {alt}",
}


def load_config(path: Path) -> dict:
    cfg = dict(DEFAULTS)
    if path and path.exists():
        with open(path, encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                merged = dict(cfg[k])
                merged.update(v)
                cfg[k] = merged
            else:
                cfg[k] = v
    if not cfg.get("document_title"):
        cfg["document_title"] = cfg.get("document_name", DEFAULTS["document_name"])
    return cfg


# ---------------------------------------------------------------- styles

def strip_base_template(doc: Document) -> None:
    """Keep a base template's STYLES + HEADERS/FOOTERS, drop body content.

    Registry template.docx files are full user documents. The export renders
    fresh body content, so the template's body paragraphs/tables must go —
    otherwise the output would prepend the template's old pages. Headers and
    footers are KEPT: the template governs its own chrome (with {{}}/[[ ]]
    placeholders already filled); the new body section links to them when
    present, otherwise a header/footer is generated from template.yaml.
    Style definitions live in the styles part and are untouched.
    """
    body_el = doc.element.body
    for child in list(body_el):
        if child.tag.endswith("}p") or child.tag.endswith("}tbl"):
            body_el.remove(child)


def ensure_code_style(doc: Document, cfg: dict):
    """Create the Code Block style ONLY if the template lacks it.

    The template governs all formatting — nothing is forced. This fallback
    definition (from yaml code_*) exists solely so fenced code has a style
    to use when the template provides none.
    """
    if "Code Block" in doc.styles:
        return doc.styles["Code Block"]
    st_cfg = cfg.get("styles", {}) or {}
    code = doc.styles.add_style("Code Block", 1)  # paragraph style
    code.base_style = doc.styles["Normal"]
    code.font.size = _cfg_pt(st_cfg, "code_size", 11)
    return code


def iter_all_paragraphs(doc: Document):
    """Yield every body paragraph, including table cells and header/footer."""
    for p in doc.paragraphs:
        yield p
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield p
    for section in doc.sections:
        for part in (section.header, section.footer):
            for p in part.paragraphs:
                yield p
            for table in part.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            yield p


try:
    from extract_template import PLACEHOLDER_RE
except ImportError:  # standalone copy — same pattern as extract_template.py
    import re as _re

    PLACEHOLDER_RE = _re.compile(
        r"\{\{\s*([A-Za-z0-9_.-]+)\s*\}\}|\[\[\s*([A-Za-z0-9_.-]+)\s*\]\]"
    )


def _token_name(m) -> str:
    return m.group(1) or m.group(2)


def _mapping_value(mapping: dict, name: str):
    """Resolved value for a placeholder, or None when unfilled."""
    if name not in mapping:
        return None
    v = mapping[name]
    if v is None:
        return None
    if isinstance(v, str) and v.strip() == "":
        return None
    if isinstance(v, (list, tuple)):
        v = ", ".join(str(x) for x in v)
    return str(v)


def collect_placeholders(doc: Document) -> set:
    """All {{name}}/[[name]] tokens in body + tables + headers/footers.

    Code Block paragraphs are skipped (literal {{ }} in code samples).
    """
    names = set()
    for p in iter_all_paragraphs(doc):
        try:
            if p.style.name == "Code Block":
                continue
        except AttributeError:
            pass
        for m in PLACEHOLDER_RE.finditer(p.text or ""):
            names.add(_token_name(m))
    return names


def substitute_placeholders(doc: Document, mapping: dict) -> set:
    """Replace tokens having a non-empty mapping value. Returns replaced names.

    Unmapped tokens are left intact for the caller to report. Run-aware:
    single-run tokens keep formatting; cross-run tokens merge into the
    first run. Code Block paragraphs are never touched.
    """
    replaced = set()
    for p in iter_all_paragraphs(doc):
        try:
            if p.style.name == "Code Block":
                continue
        except AttributeError:
            pass
        if not PLACEHOLDER_RE.search(p.text or ""):
            continue

        def rep(m):
            name = _token_name(m)
            v = _mapping_value(mapping, name)
            if v is None:
                return m.group(0)
            replaced.add(name)
            return v

        for run in p.runs:
            if PLACEHOLDER_RE.search(run.text or ""):
                run.text = PLACEHOLDER_RE.sub(rep, run.text)
        if PLACEHOLDER_RE.search(p.text or ""):
            # Token spans runs — merge into the first run (only if changed).
            merged = PLACEHOLDER_RE.sub(rep, p.text)
            if merged != p.text and p.runs:
                p.runs[0].text = merged
                for r in p.runs[1:]:
                    r.text = ""


def add_heading_left(doc: Document, text: str, level: int, code_font: str = ""):
    """Body headings use the template's Heading styles untouched (inline parsed)."""
    h = doc.add_heading(level=level)
    add_spans(h, parse_inline(text), code_font)
    return h


# ---------------------------------------------------------------- front matter (removed)

# Cover / control / TOC auto-pages and generated header/footer were removed:
# the template governs its own pages and chrome. Its headers/footers are kept
# (placeholders filled); page geometry still comes from the yaml page block.


# ---------------------------------------------------------------- page geometry

def apply_page_geometry(doc: Document, cfg: dict) -> None:
    """Apply the yaml page block (size/orientation/margins/distances) to every
    existing section. Headers/footers are the template's own — never generated.
    """
    pg = cfg.get("page", {}) or {}
    size = str(pg.get("size", "A4")).upper()
    orientation = str(pg.get("orientation", "portrait")).lower()
    if size == "LETTER":
        w_cm, h_cm = 21.59, 27.94
    else:  # A4 (default) or anything unknown
        w_cm, h_cm = 21.0, 29.7
    if orientation == "landscape":
        w_cm, h_cm = h_cm, w_cm
    for s in doc.sections:
        s.page_width = Cm(w_cm)
        s.page_height = Cm(h_cm)
        s.top_margin = _cfg_cm(pg, "margin_top_cm", 2.54, "page")
        s.bottom_margin = _cfg_cm(pg, "margin_bottom_cm", 2.54, "page")
        s.left_margin = _cfg_cm(pg, "margin_left_cm", 2.0, "page")
        s.right_margin = _cfg_cm(pg, "margin_right_cm", 2.0, "page")
        s.header_distance = _cfg_cm(pg, "header_distance_cm", 1.27, "page")
        s.footer_distance = _cfg_cm(pg, "footer_distance_cm", 1.27, "page")


# ---------------------------------------------------------------- input reading

def read_text_tolerant(path: Path) -> str:
    """Windows Notepad often saves UTF-16; try common encodings in order."""
    for enc in ("utf-8-sig", "utf-16", "cp1258", "cp1252"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise SystemExit(
        f"LỖI: không đọc được '{path.name}' (encoding lạ). "
        "Hãy lưu lại dạng UTF-8.")


def read_source(path: Path) -> Tuple[str, str]:
    ext = path.suffix.lower()
    if ext in (".md", ".markdown", ".txt", ".text"):
        return ext, read_text_tolerant(path)
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            raise SystemExit(
                "LỖI: file PDF cần thư viện 'pypdf' để trích xuất chữ. "
                "Cài đặt: pip install pypdf — hoặc cung cấp bản .md/.txt.")
        reader = PdfReader(str(path))
        text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
        if not text:
            raise SystemExit(
                "LỖI: PDF này không trích xuất được chữ (file scan/ảnh). "
                "Hãy cung cấp bản .md/.txt.")
        return ext, text
    raise SystemExit(f"LỖI: định dạng '{ext}' chưa hỗ trợ. Hãy dùng .md / .txt / .pdf.")


# ---------------------------------------------------------------- markdown / plain-text rendering

def _add_md_table(doc: Document, rows: List[List[str]], code_font: str = ""):
    if not rows:
        return
    tbl = doc.add_table(rows=1, cols=len(rows[0]))
    try:
        tbl.style = "Table Grid"
    except KeyError:
        pass
    for cell, text in zip(tbl.rows[0].cells, rows[0]):
        cell.text = ""
        add_spans(cell.paragraphs[0], parse_inline(text), code_font)
    for row in rows[1:]:
        cells = tbl.add_row().cells
        for i in range(len(rows[0])):
            cells[i].text = ""
            add_spans(cells[i].paragraphs[0],
                      parse_inline(row[i] if i < len(row) else ""), code_font)


def caption_style_name(doc: Document) -> str:
    """Caption style of the template, else Normal. Never forced."""
    return "Caption" if "Caption" in doc.styles else "Normal"


# ---------------------------------------------------------------- inline markdown

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_ESCAPABLE = "\\`*_~[]"


def parse_inline(text: str):
    """Split markdown inline markup into (text, flags, url) spans.

    Flags subset of {"bold", "italic", "code", "strike"}; url set for links.
    Nesting (bold containing code/italic/link), backslash escapes, and
    unclosed markers (kept literal) are handled.
    """
    spans: List[Tuple[str, frozenset, Optional[str]]] = []

    def emit(t: str, flags, url):
        if t:
            spans.append((t, flags, url))

    def rec(s: str, flags, url):
        i, n = 0, len(s)
        buf: List[str] = []

        def flush():
            emit("".join(buf), flags, url)
            buf.clear()

        while i < n:
            if s[i] == "\\" and i + 1 < n and s[i + 1] in _ESCAPABLE:
                buf.append(s[i + 1])
                i += 2
                continue
            if s.startswith("**", i):
                j = s.find("**", i + 2)
                if j == -1:
                    buf.append("**")
                    i += 2
                    continue
                flush()
                rec(s[i + 2:j], flags | {"bold"}, url)
                i = j + 2
                continue
            if s.startswith("~~", i):
                j = s.find("~~", i + 2)
                if j == -1:
                    buf.append("~~")
                    i += 2
                    continue
                flush()
                rec(s[i + 2:j], flags | {"strike"}, url)
                i = j + 2
                continue
            if s[i] == "*":
                j = s.find("*", i + 1)
                if j == -1:
                    buf.append("*")
                    i += 1
                    continue
                flush()
                rec(s[i + 1:j], flags | {"italic"}, url)
                i = j + 1
                continue
            if s[i] == "`":
                j = s.find("`", i + 1)
                if j == -1:
                    buf.append("`")
                    i += 1
                    continue
                flush()
                emit(s[i + 1:j], flags | {"code"}, url)
                i = j + 1
                continue
            if s[i] == "[":
                lm = _LINK_RE.match(s[i:])
                if not lm:
                    buf.append("[")
                    i += 1
                    continue
                flush()
                rec(lm.group(1), flags, lm.group(2))
                i += len(lm.group(0))
                continue
            buf.append(s[i])
            i += 1
        flush()

    rec(text, frozenset(), None)
    return spans


def _add_hyperlink_run(paragraph, url: str, text: str, flags) -> None:
    """Clickable hyperlink run; Hyperlink char style first, else blue+underline."""
    run = paragraph.add_run(text)
    if "bold" in flags:
        run.bold = True
    if "italic" in flags:
        run.italic = True
    try:
        run.style = "Hyperlink"
    except (KeyError, ValueError):
        run.font.color.rgb = HYPERLINK_BLUE
        run.font.underline = True
    try:
        r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    except Exception:
        return  # keep the plain run when relating fails
    r_el = run._r
    r_el.getparent().remove(r_el)
    hlink = OxmlElement("w:hyperlink")
    hlink.set(qn("r:id"), r_id)
    hlink.append(r_el)
    paragraph._p.append(hlink)


def add_spans(paragraph, spans, code_font: str = "") -> None:
    """Append parsed inline spans as runs. Values stay literal (no re-parse)."""
    for text, flags, url in spans:
        if url:
            _add_hyperlink_run(paragraph, url, text, flags)
            continue
        run = paragraph.add_run(text)
        if "bold" in flags:
            run.bold = True
        if "italic" in flags:
            run.italic = True
        if "strike" in flags:
            run.font.strike = True
        if "code" in flags and code_font:
            run.font.name = code_font


def add_rich_paragraph(doc: Document, text: str, style=None, code_font: str = ""):
    """Paragraph with inline markdown parsed; style from the template."""
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    add_spans(p, parse_inline(text), code_font)
    return p


def quote_style_name(doc: Document):
    """Quote-ish style of the template, else None (caller indents instead)."""
    for name in ("Quote", "Block Text", "Intense Quote"):
        if name in doc.styles:
            return name
    return None


def render_markdown(doc: Document, text: str, src_dir: Path, caption_format: str,
                    code_font: str = ""):
    lines = text.splitlines()
    i = 0
    table_buf: List[List[str]] = []
    fig_no = [0]
    quote_style = quote_style_name(doc)

    def flush_table():
        nonlocal table_buf
        if table_buf:
            # Drop the md separator row (|---|---|).
            data = [r for r in table_buf if not all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in r)]
            _add_md_table(doc, data, code_font)
            table_buf = []

    def add_figure(src: str, alt: str):
        """Centered figure + caption below (template's Caption style).
        Image files must live in assets/ (or any resolvable path) —
        never base64 embeds."""
        cap_style = caption_style_name(doc)
        ip = (src_dir / src).resolve() if not Path(src).is_absolute() else Path(src)
        if ip.exists():
            try:
                fig_no[0] += 1
                pic_p = doc.add_paragraph()
                pic_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pic_p.add_run().add_picture(str(ip), width=Inches(5.5))
                cap = doc.add_paragraph(style=cap_style)
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_spans(cap, parse_inline(caption_format.format(n=fig_no[0], alt=alt or ip.name)),
                          code_font)
                return
            except Exception:
                pass
        p = doc.add_paragraph(style=cap_style)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_spans(p, parse_inline(f"[{alt or src}]"), code_font)

    in_code = False
    code_buf: List[str] = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                p = doc.add_paragraph("\n".join(code_buf), style="Code Block")
                code_buf = []
                in_code = False
            else:
                flush_table()
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line.rstrip("\n"))
            i += 1
            continue
        if not stripped:
            flush_table()
            i += 1
            continue
        if stripped == "---":
            # No horizontal rules, no page break: chapters are separated by
            # headings + whitespace only (docx-style.md §2).
            flush_table()
            doc.add_paragraph()
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if m:
            flush_table()
            level = min(len(m.group(1)), 6)
            add_heading_left(doc, m.group(2).strip(), level=level, code_font=code_font)
            i += 1
            continue
        if stripped.startswith(">"):
            flush_table()
            qlines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                qlines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            if quote_style:
                qp = doc.add_paragraph(style=quote_style)
            else:
                qp = doc.add_paragraph()
                qp.paragraph_format.left_indent = QUOTE_FALLBACK_INDENT
            add_spans(qp, parse_inline(" ".join(qlines)), code_font)
            continue
        if re.match(r"^(\|.*\|)\s*$", stripped) and "|" in stripped:
            cells = [c.strip() for c in stripped.strip().strip("|").split("|")]
            table_buf.append(cells)
            i += 1
            continue
        else:
            flush_table()
        if re.match(r"^([-*])\s+", stripped):
            add_rich_paragraph(doc, re.sub(r"^[-*]\s+", "", stripped),
                               style="List Bullet", code_font=code_font)
            i += 1
            continue
        if re.match(r"^\d+[.)]\s+", stripped):
            add_rich_paragraph(doc, re.sub(r"^\d+[.)]\s+", "", stripped),
                               style="List Number", code_font=code_font)
            i += 1
            continue
        img = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", stripped)
        if img:
            flush_table()
            add_figure(img.group(2), img.group(1))
            i += 1
            continue
        add_rich_paragraph(doc, stripped, code_font=code_font)
        i += 1
    flush_table()
    if in_code:  # Unclosed fence — still emit it.
        p = doc.add_paragraph("\n".join(code_buf), style="Code Block")


def render_plain_text(doc: Document, text: str):
    """txt + extracted pdf: a blank line starts a new paragraph; numbered or
    ALL-CAPS lines are heuristically promoted to headings."""
    for raw in re.split(r"\n\s*\n", text.strip()):
        block = raw.strip()
        if not block:
            continue
        first = block.splitlines()[0].strip()
        if re.match(r"^\d+(\.\d+)*\.?\s+\S+", first) and len(first) < 120:
            level = min(first.count(".") + 1, 6)
            add_heading_left(doc, re.sub(r"^\d+(\.\d+)*\.?\s+", "", first), level=level)
            rest = "\n".join(block.splitlines()[1:]).strip()
            if rest:
                doc.add_paragraph(rest)
        elif first.isupper() and 4 < len(first) < 120:
            add_heading_left(doc, first.title(), level=1)
            rest = "\n".join(block.splitlines()[1:]).strip()
            if rest:
                doc.add_paragraph(rest)
        else:
            doc.add_paragraph(block)


# ---------------------------------------------------------------- main

def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="haro-docx-writer enterprise .docx builder")
    ap.add_argument("--input", required=True, help="source .md/.txt/.pdf")
    ap.add_argument("--output", required=True, help="output .docx path")
    ap.add_argument("--config", default="", help="config yaml (.haro-docx-writer template.yaml or legacy config)")
    ap.add_argument("--base-template", default="", help="base .docx style template (template.docx of a registry entry)")
    ap.add_argument("--template-id", default="", help="registry id (vd congty-a): resolves --config/--base-template automatically; local wins over global")
    ap.add_argument("--project-root", default=".", help="project root for --template-id local scope")
    ap.add_argument("--param", action="append", default=[],
                    help="placeholder value override name=value (repeatable, not saved to yaml)")
    return ap.parse_args(argv)


def build_mapping(cfg: dict, cli_params: Optional[List[str]] = None) -> dict:
    """Values for {{name}}/[[name]] substitution.

    Priority: --param overrides > placeholders.<name>.value (non-empty) >
    top-level yaml scalar of the same name. Unlisted names stay unfilled.
    """
    mapping: dict = {}
    for k, v in (cfg or {}).items():
        if k.startswith("_"):
            continue
        if isinstance(v, (str, int, float)) and not isinstance(v, bool):
            mapping[k] = v
    for name, spec in ((cfg.get("placeholders", {}) or {}).items()):
        val = spec.get("value", "") if isinstance(spec, dict) else spec
        if val is None or (isinstance(val, str) and val.strip() == ""):
            continue
        mapping[name] = val
    for item in cli_params or []:
        if "=" not in item:
            print(f"LỖI: --param phải dạng name=value (nhận được '{item}').", file=sys.stderr)
            raise SystemExit(2)
        k, v = item.split("=", 1)
        mapping[k.strip()] = v.strip()
    return mapping


def main(argv=None) -> int:
    # Allow Vietnamese diacritics on Windows consoles (default cp1252 would crash).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass

    args = parse_args(argv)
    src = Path(args.input)
    if not src.exists():
        print(f"LỖI: không tìm thấy input '{src}'.", file=sys.stderr)
        return 2
    if args.template_id:
        if resolve_template is None:
            print("LỖI: --template-id cần module template_store.py cùng thư mục scripts.", file=sys.stderr)
            return 2
        hit = resolve_template(args.template_id, Path(args.project_root))
        if not hit:
            print(f"LỖI: không tìm thấy mẫu '{args.template_id}'. Chạy /haro-docx-writer --list.", file=sys.stderr)
            return 2
        if not args.config and hit["yaml"].exists():
            args.config = str(hit["yaml"])
        if not args.base_template and hit["docx"].exists():
            args.base_template = str(hit["docx"])
    cfg = load_config(Path(args.config)) if args.config else dict(DEFAULTS)
    mapping = build_mapping(cfg, args.param)
    caption_format = str(cfg.get("figure_caption", "Figure {n}: {alt}"))

    if args.base_template:
        tpl = Path(args.base_template)
        if not tpl.exists():
            print(f"LỖI: không tìm thấy template '{tpl}'.", file=sys.stderr)
            return 2
        doc = Document(str(tpl))
        substitute_placeholders(doc, mapping)
        strip_base_template(doc)
    else:
        doc = Document()

    ensure_code_style(doc, cfg)
    apply_page_geometry(doc, cfg)

    ext, text = read_source(src)
    code_font = str((cfg.get("styles", {}) or {}).get("code_font", ""))
    if ext in (".md", ".markdown"):
        render_markdown(doc, text, src.parent, caption_format, code_font)
    else:
        render_plain_text(doc, text)

    substitute_placeholders(doc, mapping)
    missing = sorted(
        n for n in collect_placeholders(doc)
        if _mapping_value(mapping, n) is None
    )
    if missing:
        print("LỖI: còn placeholder chưa có giá trị nên không render:",
              file=sys.stderr)
        for n in missing:
            print(f"  - {n}", file=sys.stderr)
        print("Hỏi user để map/nhập giá trị rồi chạy lại với --param name=value "
              "hoặc lưu vào YAML rồi chạy lại.", file=sys.stderr)
        return 2

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() != ".docx":
        out = out.with_suffix(".docx")
    doc.save(str(out))
    print(f"Xong: {out} (từ {src.name}, mẫu {'dự án' if args.config else 'mặc định'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
