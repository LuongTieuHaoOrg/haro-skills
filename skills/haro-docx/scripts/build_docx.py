#!/usr/bin/env python3
"""Build an enterprise-standard .docx from markdown/text/pdf (+ optional base template).

Usage:
    python build_docx.py --input <file.md|txt|pdf> --output <out.docx>
                         --config <config.yaml> [--base-template <tpl.docx>]

Implements skills/haro-docx/shared/docx-style.md. This is the ONLY supported
way to produce .docx in haro-docx — agents must call this script, never
hand-craft documents.
Requires: python-docx, pyyaml. Optional: pypdf (only for .pdf input).

Language convention: code, comments and docstrings are in English; every
string the user sees (document content, console messages, errors) is in
Vietnamese with full diacritics.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

import yaml
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Inches, Pt, RGBColor

# Single-ink standard: every run is black; the only fills allowed are the
# light-grey table-header background and the code-block shading.
BLACK = "000000"
TABLE_HEAD_BG = "D9D9D9"
CODE_BG = "F2F2F2"
BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"

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
    "header": {"logo_path": ""},
    "styles": {
        "body_font": BODY_FONT,
        "heading_color": BLACK,
        "code_font": CODE_FONT,
        "body_size": 12,
        "h1_size": 14,
        "h2_size": 13,
        "h3_size": 12,
        "code_size": 11,
    },
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


# ---------------------------------------------------------------- low-level xml helpers

def _fld_char(run, val: str):
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), val)
    run._r.append(fld)


def _instr(run, text: str):
    inst = OxmlElement("w:instrText")
    inst.set(qn("xml:space"), "preserve")
    inst.text = text
    run._r.append(inst)


def add_toc_field(paragraph, levels: str = "1-3"):
    r = paragraph.add_run()
    _fld_char(r, "begin")
    r = paragraph.add_run()
    _instr(r, f'TOC \\o "{levels}" \\h \\z \\u')
    r = paragraph.add_run()
    _fld_char(r, "separate")
    r = paragraph.add_run("Mục lục sẽ hiển thị khi mở bằng Word (chuột phải → Update Field).")
    r = paragraph.add_run()
    _fld_char(r, "end")


def add_page_field(paragraph, prefix: str = "Trang ", suffix: str = ""):
    if prefix:
        paragraph.add_run(prefix)
    r = paragraph.add_run()
    _fld_char(r, "begin")
    r = paragraph.add_run()
    _instr(r, "PAGE")
    r = paragraph.add_run()
    _fld_char(r, "end")
    paragraph.add_run(" / ")
    r = paragraph.add_run()
    _fld_char(r, "begin")
    r = paragraph.add_run()
    _instr(r, "NUMPAGES")
    r = paragraph.add_run()
    _fld_char(r, "end")
    if suffix:
        paragraph.add_run(suffix)


def set_cell_shading(cell, fill: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def set_table_borders_none(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)


def set_run_font(run, name: str, size=None, bold=None, italic=None, color: str = BLACK):
    """Force the font at run level so a --base-template theme can never override it."""
    run.font.name = name
    # Also set eastAsia + cs slots (Word falls back to them for some glyphs).
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for slot in ("w:ascii", "w:hAnsi", "w:cs"):
        rFonts.set(qn(slot), name)
    if size is not None:
        run.font.size = size
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def set_cell_text(cell, text: str, bold=False, size=None, color: str = BLACK,
                  align=None, italic=False, font: str = BODY_FONT):
    cell.text = ""
    p = cell.paragraphs[0]
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    set_run_font(run, font, size=size, bold=bold, italic=italic, color=color)
    return p


# ---------------------------------------------------------------- styles

def ensure_styles(doc: Document, cfg: dict):
    st_cfg = cfg.get("styles", {})
    body_font = st_cfg.get("body_font", BODY_FONT)
    code_font = st_cfg.get("code_font", CODE_FONT)
    body_size = Pt(st_cfg.get("body_size", 12))
    h_sizes = {
        "Heading 1": Pt(st_cfg.get("h1_size", 14)),
        "Heading 2": Pt(st_cfg.get("h2_size", 13)),
        "Heading 3": Pt(st_cfg.get("h3_size", 12)),
    }

    normal = doc.styles["Normal"]
    normal.font.name = body_font
    normal.font.size = body_size
    normal.font.color.rgb = RGBColor.from_string(BLACK)
    pf = normal.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(6)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    for name, size in h_sizes.items():
        st = doc.styles[name]
        st.font.name = body_font
        st.font.size = size
        st.font.bold = True
        st.font.italic = False
        st.font.color.rgb = RGBColor.from_string(BLACK)
        st.font.all_caps = False
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.space_after = Pt(6)

    if "Code Block" not in doc.styles:
        code = doc.styles.add_style("Code Block", 1)  # paragraph style
    else:
        code = doc.styles["Code Block"]
    code.base_style = doc.styles["Normal"]
    code.font.name = code_font
    code.font.size = Pt(st_cfg.get("code_size", 11))
    code.font.color.rgb = RGBColor.from_string(BLACK)
    code.paragraph_format.space_after = Pt(6)
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


def finalize_fonts(doc: Document, cfg: dict):
    """Run-level font forcing: Times New Roman + black everywhere, Consolas
    for code. Neutralises any --base-template theme fonts. Sizes, bold and
    italic set during the build are preserved — only the family and the
    colour are forced."""
    st_cfg = cfg.get("styles", {})
    body_font = st_cfg.get("body_font", BODY_FONT)
    code_font = st_cfg.get("code_font", CODE_FONT)
    code_size = Pt(st_cfg.get("code_size", 11))
    h_sizes = {
        "Heading 1": Pt(st_cfg.get("h1_size", 14)),
        "Heading 2": Pt(st_cfg.get("h2_size", 13)),
        "Heading 3": Pt(st_cfg.get("h3_size", 12)),
    }
    for p in iter_all_paragraphs(doc):
        if p.style.name == "Code Block":
            for run in p.runs:
                set_run_font(run, code_font, size=code_size, color=BLACK)
        elif p.style.name in h_sizes:
            for run in p.runs:
                set_run_font(run, body_font, size=h_sizes[p.style.name],
                             bold=True, italic=run.italic, color=BLACK)
        else:
            for run in p.runs:
                set_run_font(run, body_font,
                             size=run.font.size, bold=run.bold, italic=run.italic,
                             color=BLACK)


def add_heading_left(doc: Document, text: str, level: int):
    """Body headings are always explicitly left-aligned (cover stays centered)."""
    h = doc.add_heading(text, level=level)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return h


def shade_paragraph(paragraph, fill: str):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


# ---------------------------------------------------------------- front matter

def build_cover(doc: Document, cfg: dict, base_dir: Path):
    logo = (cfg.get("header") or {}).get("logo_path", "") or ""
    if logo:
        lp = (base_dir / logo).resolve() if not Path(logo).is_absolute() else Path(logo)
        if lp.exists():
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(str(lp), width=Cm(4))
        # Missing logo: silently skip (export.md tells the agent to note it).

    for _ in range(2):
        doc.add_paragraph()

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(cfg["document_title"])
    set_run_font(r, BODY_FONT, size=Pt(24), bold=True)

    s = doc.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = s.add_run(cfg["solution_name"])
    set_run_font(r, BODY_FONT, size=Pt(14))

    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(cfg["company_name"])
    set_run_font(r, BODY_FONT, size=Pt(12))

    doc.add_paragraph()
    meta = doc.add_table(rows=1, cols=2)
    meta.style = "Table Grid"
    rows = [
        ("Phiên bản", str(cfg.get("version", ""))),
        ("Ngày", str(cfg.get("date", ""))),
        ("Tác giả", ", ".join(cfg.get("authors", [])) or "—"),
        ("Trạng thái", str(cfg.get("status", ""))),
    ]
    for k, v in rows:
        cells = meta.add_row().cells
        set_cell_text(cells[0], k, bold=True)
        set_cell_text(cells[1], v)

    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = note.add_run("Tài liệu lưu hành nội bộ.")
    set_run_font(r, BODY_FONT, size=Pt(9), italic=True)
    doc.add_page_break()


def _styled_header_row(cells, texts):
    """Header row: bold black on the single light-grey fill. No other colours."""
    for cell, text in zip(cells, texts):
        set_cell_text(cell, text, bold=True, color=BLACK)
        set_cell_shading(cell, TABLE_HEAD_BG)


def build_control_pages(doc: Document, cfg: dict):
    add_heading_left(doc, "Lịch sử thay đổi", level=1)
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = "Table Grid"
    _styled_header_row(tbl.rows[0].cells, ["Phiên bản", "Ngày", "Nội dung", "Người sửa"])
    first_author = (cfg.get("authors") or ["—"])[0]
    row = tbl.add_row().cells
    row[0].text = str(cfg.get("version", "1.0"))
    row[1].text = str(cfg.get("date", ""))
    row[2].text = "Danh mục ban đầu"
    row[3].text = first_author

    doc.add_paragraph()
    add_heading_left(doc, "Người phụ trách", level=1)
    tbl2 = doc.add_table(rows=1, cols=3)
    tbl2.style = "Table Grid"
    _styled_header_row(tbl2.rows[0].cells, ["Vai trò", "Họ tên", "Chữ ký"])
    for role, people in (("Biên soạn", cfg.get("authors", [])),
                         ("Kiểm tra", cfg.get("reviewers", [])),
                         ("Phê duyệt", cfg.get("approvers", []))):
        names = ", ".join(people) if people else "—"
        cells = tbl2.add_row().cells
        cells[0].text = role
        cells[1].text = names
        cells[2].text = ""
    doc.add_page_break()


def build_toc(doc: Document):
    add_heading_left(doc, "Mục lục", level=1)
    add_toc_field(doc.add_paragraph())
    hint = doc.add_paragraph()
    r = hint.add_run("Mở file → chuột phải vào dòng trên → Update Field để hiện menu danh mục.")
    set_run_font(r, BODY_FONT, size=Pt(9), italic=True)
    doc.add_page_break()


# ---------------------------------------------------------------- header/footer (body section only)

def setup_body_section(doc: Document, cfg: dict, base_dir: Path):
    # New section so cover/control/TOC stay header-free.
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False

    # A4 + margins on every section.
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(2.54)
        s.bottom_margin = Cm(2.54)
        s.left_margin = Cm(2.0)
        s.right_margin = Cm(2.0)
        s.header_distance = Cm(1.27)
        s.footer_distance = Cm(1.27)

    # Header: left logo | right 2 lines (document name / company name).
    ht = section.header.add_table(rows=1, cols=2, width=Inches(6.5))
    set_table_borders_none(ht)
    logo = (cfg.get("header") or {}).get("logo_path", "") or ""
    if logo:
        lp = (base_dir / logo).resolve() if not Path(logo).is_absolute() else Path(logo)
        if lp.exists():
            ht.cell(0, 0).paragraphs[0].add_run().add_picture(str(lp), height=Cm(1.2))
    right = ht.cell(0, 1).paragraphs[0]
    right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = right.add_run(cfg["document_name"])
    set_run_font(r1, BODY_FONT, size=Pt(9), bold=True)
    right.add_run().add_break()
    r2 = right.add_run(cfg["company_name"])
    set_run_font(r2, BODY_FONT, size=Pt(8))

    # Footer: left page X/Y | right solution name.
    ft = section.footer.add_table(rows=1, cols=2, width=Inches(6.5))
    set_table_borders_none(ft)
    left_p = ft.cell(0, 0).paragraphs[0]
    add_page_field(left_p)
    for run in left_p.runs:
        set_run_font(run, BODY_FONT, size=Pt(8))
    right_p = ft.cell(0, 1).paragraphs[0]
    right_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = right_p.add_run(cfg["solution_name"])
    set_run_font(r, BODY_FONT, size=Pt(8), italic=True)
    return section


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


def read_source(path: Path) -> tuple[str, str]:
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

def _add_md_table(doc: Document, rows: list[list[str]]):
    if not rows:
        return
    tbl = doc.add_table(rows=1, cols=len(rows[0]))
    tbl.style = "Table Grid"
    _styled_header_row(tbl.rows[0].cells, rows[0])
    for row in rows[1:]:
        cells = tbl.add_row().cells
        for i in range(len(rows[0])):
            cells[i].text = row[i] if i < len(row) else ""


def render_markdown(doc: Document, text: str, src_dir: Path):
    lines = text.splitlines()
    i = 0
    table_buf: list[list[str]] = []
    fig_no = [0]  # mutable counter for "Hình N" captions

    def flush_table():
        nonlocal table_buf
        if table_buf:
            # Drop the md separator row (|---|---|).
            data = [r for r in table_buf if not all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in r)]
            _add_md_table(doc, data)
            table_buf = []

    def add_figure(src: str, alt: str):
        """Centered figure + italic caption below. Image files must live in
        assets/ (or any resolvable path) — never base64 embeds."""
        ip = (src_dir / src).resolve() if not Path(src).is_absolute() else Path(src)
        if ip.exists():
            try:
                fig_no[0] += 1
                pic_p = doc.add_paragraph()
                pic_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pic_p.add_run().add_picture(str(ip), width=Inches(5.5))
                cap = doc.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = cap.add_run(f"Hình {fig_no[0]}: {alt or ip.name}")
                set_run_font(run, BODY_FONT, size=Pt(11), italic=True)
                return
            except Exception:
                pass
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"[Hình minh hoạ: {alt or src}]")
        set_run_font(run, BODY_FONT, size=Pt(11), italic=True)

    in_code = False
    code_buf: list[str] = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                p = doc.add_paragraph("\n".join(code_buf), style="Code Block")
                shade_paragraph(p, CODE_BG)
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
            level = min(len(m.group(1)), 3)
            add_heading_left(doc, m.group(2).strip(), level=level)
            i += 1
            continue
        if re.match(r"^(\|.*\|)\s*$", stripped) and "|" in stripped:
            cells = [c.strip() for c in stripped.strip().strip("|").split("|")]
            table_buf.append(cells)
            i += 1
            continue
        else:
            flush_table()
        if re.match(r"^([-*])\s+", stripped):
            doc.add_paragraph(re.sub(r"^[-*]\s+", "", stripped), style="List Bullet")
            i += 1
            continue
        if re.match(r"^\d+[.)]\s+", stripped):
            doc.add_paragraph(re.sub(r"^\d+[.)]\s+", "", stripped), style="List Number")
            i += 1
            continue
        img = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", stripped)
        if img:
            flush_table()
            add_figure(img.group(2), img.group(1))
            i += 1
            continue
        doc.add_paragraph(stripped)
        i += 1
    flush_table()
    if in_code:  # Unclosed fence — still emit it.
        p = doc.add_paragraph("\n".join(code_buf), style="Code Block")
        shade_paragraph(p, CODE_BG)


def render_plain_text(doc: Document, text: str):
    """txt + extracted pdf: a blank line starts a new paragraph; numbered or
    ALL-CAPS lines are heuristically promoted to headings."""
    for raw in re.split(r"\n\s*\n", text.strip()):
        block = raw.strip()
        if not block:
            continue
        first = block.splitlines()[0].strip()
        if re.match(r"^\d+(\.\d+)*\.?\s+\S+", first) and len(first) < 120:
            level = min(first.count(".") + 1, 3)
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
    ap = argparse.ArgumentParser(description="haro-docx enterprise .docx builder")
    ap.add_argument("--input", required=True, help="source .md/.txt/.pdf")
    ap.add_argument("--output", required=True, help="output .docx path")
    ap.add_argument("--config", default="", help="config yaml (.haro-docx/config.yaml or template default)")
    ap.add_argument("--base-template", default="", help="base .docx style template (from --template picker)")
    return ap.parse_args(argv)


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
    cfg = load_config(Path(args.config)) if args.config else dict(DEFAULTS)
    base_dir = Path(args.config).parent.resolve() if args.config and Path(args.config).exists() else Path.cwd()

    if args.base_template:
        tpl = Path(args.base_template)
        if not tpl.exists():
            print(f"LỖI: không tìm thấy template '{tpl}'.", file=sys.stderr)
            return 2
        doc = Document(str(tpl))
    else:
        doc = Document()

    ensure_styles(doc, cfg)
    build_cover(doc, cfg, base_dir)
    build_control_pages(doc, cfg)
    build_toc(doc)
    setup_body_section(doc, cfg, base_dir)

    ext, text = read_source(src)
    if ext in (".md", ".markdown"):
        render_markdown(doc, text, src.parent)
    else:
        render_plain_text(doc, text)

    finalize_fonts(doc, cfg)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() != ".docx":
        out = out.with_suffix(".docx")
    doc.save(str(out))
    print(f"Xong: {out} (từ {src.name}, cấu hình {'dự án' if args.config else 'mặc định'})")
    print("Lưu ý: mở file -> chuột phải vào Mục lục -> Update Field.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
