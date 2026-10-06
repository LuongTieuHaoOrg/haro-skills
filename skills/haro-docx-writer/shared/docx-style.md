# DOCX Style — Enterprise Standard (Haro Docx, normative)

> `scripts/build_docx.py` implements this file. The agent must NOT restyle
> by hand — change this file plus the script instead.

## 1. Font and color (defaults, whole document)

- Single typeface for all text: `Times New Roman`. Single ink: black `000000`.
  No other font or color anywhere (including header, footer, cover, tables,
  TOC).
- H1: 14pt, bold. H2: 13pt, bold. H3: 12pt, bold. H4: 12pt, bold.
  H5: 11pt, bold. H6: 11pt, bold. Sizes come from the template's
  `styles.h1_size` … `styles.h6_size`.
- Body: 12pt, regular, line spacing and paragraph spacing from the template's
  `styles.body_line_spacing` / `body_space_before` / `body_space_after`.
- Bulleted/numbered lists use the `List Bullet` / `List Number` styles:
  indent from `styles.bullet_indent_cm`, trailing space from
  `styles.bullet_space_after`, left-aligned.
- Code / endpoints / parameters: `Consolas` 11pt inside a light-grey frame,
  original English kept as-is (the skill only formats, never translates).
- Emphasis via bold or italic only — never a different font or color.
- Fonts are forced at run level on export: every text run carries its font
  directly, so a Word template theme (`--base-template`) can never override
  headings or body text.
- Units in YAML: bare numbers keep legacy meaning (font/spacing sizes = pt,
  margins/indents = cm, `body_line_spacing` is a unitless factor). Strings
  with a unit convert automatically: `"12pt"`, `"2.54cm"`, `"25mm"`, `"1in"`
  (`1in = 2.54cm = 25.4mm = 72pt`). Unknown units or bad formats are refused
  with a clear error — never guessed.

## 2. Alignment and spacing

- Body text justified on both sides. Headings left-aligned. The cover page is
  fully centered.
- Page geometry comes from the template's `page` block: paper size
  (`A4`/`Letter`), orientation, 4 margins, header/footer distances.
  Defaults: A4 portrait, margins 2.54/2.54/2.0/2.0cm, distances 1.27cm.
- No horizontal separator rules (no horizontal lines, no paragraph borders).
  Chapters are separated by headings plus whitespace (space before/after). A
  `---` line in markdown becomes just a blank paragraph.

## 3. Cover page (page 1, no header/footer, centered)

Centered, from top: optional logo (max 3cm) → `DOCUMENT_TITLE`
(`cover.title_size`, default 24pt bold black) → `SOLUTION_NAME`
(`cover.solution_size`, 14pt) → `COMPANY_NAME` (`cover.company_size`, 12pt)
→ meta table (Phiên bản / Ngày / Tác giả / Trạng thái) → note
`Tài liệu lưu hành nội bộ` (`cover.note_size`, 9pt). The cover ends with
a page break.

## 4. Control pages (page 2–3, no header/footer)

- `Lịch sử thay đổi` — 4-column table (Phiên bản / Ngày / Nội dung / Người sửa),
  header row bold on the single light-grey fill. Seeds one row from config
  (`version`, `date`, `Danh mục ban đầu`, `authors[0]`).
- `Người phụ trách` — 3-column table (Vai trò / Họ tên / Chữ ký) with rows
  Biên soạn (authors), Kiểm tra (reviewers), Phê duyệt (approvers).
- Every table uses `Table Grid` (full borders), repeating header row, no
  merged cells, no fill color other than the header row's light grey.

## 5. TOC page ("Mục lục")

- Heading `Mục lục` plus a real Word `TOC \o "1-6" \h \z \u` field paragraph so
  Word fills in page numbers on open (levels from the template's
  `toc_levels`, default `"1-6"`). Followed by an instructional italic line:
  `Mở file → chuột phải → Update Field để hiện menu danh mục.`
- Ends with a page break; body sections start after it.

## 6. Header (content pages only — cover/control/TOC have none)

Two-column borderless table: left cell (30%) = logo image if configured
(max height 1.2cm), else empty; right cell (70%) right-aligned with 2 lines:
line 1 = `DOCUMENT_NAME` bold (`header_footer.doc_name_size`, 9pt),
line 2 = `COMPANY_NAME` regular (`header_footer.company_size`, 8pt).
All black, Times New Roman. Header distance from `page.header_distance_cm`.

## 7. Footer (content pages only)

Two-column borderless table: left = `Trang <PAGE> / <NUMPAGES>` field codes
(`header_footer.page_size`, 8pt); right cell right-aligned =
`SOLUTION_NAME` (`header_footer.solution_size`, 8pt italic).
All black, Times New Roman. Footer distance from `page.footer_distance_cm`.

## 8. Body mapping (md/txt → docx)

| Source | Output |
|--------|--------|
| `#` … `######` | Heading 1–6, left-aligned |
| plain paragraph | Normal, justified |
| `- ` / `* ` / `1.` | List Bullet / List Number, left-aligned |
| `\| a \| b \|` | Table Grid with full borders, first row = bold + light-grey fill |
| fenced ` ``` ` | Code style (Consolas 11pt, grey background, English kept as-is) |
| `![alt](path)` | Centered figure + caption right below (`Hình N: alt`, italic 11pt). Image files must live under `assets/`, never base64 embeds; an unresolvable path becomes an italic placeholder line instead |
| `---` | Blank paragraph (whitespace), NEVER a page break or a rule line |

PDF input is plain extracted text: a blank line starts a new paragraph, and
ALL-CAPS or numbered (`1.`, `1.1`) lines are heuristically promoted to headings.

## 9. Template registry mapping (extract / validate / update)

Each registry entry keeps `template.docx` (style source) + `template.yaml`
(meta + params) + `content.txt` (machine dump of the docx text/tables/
headers/footers/image list). `scripts/extract_template.py` fills the yaml
styles and writes the dump; the AGENT reads the dump to understand the
template's purpose (free-form, cited) and proposes content params for the
user to approve — the script never guesses purpose or values.
`scripts/validate_template.py` compares yaml vs docx;
`scripts/update_template.py` pushes yaml styles back into the docx.

| YAML key | DOCX source (style-level only) |
|----------|-------------------------------|
| `styles.body_font` / `styles.body_size` | `Normal` style font name / size |
| `styles.body_line_spacing` / `body_space_before` / `body_space_after` | `Normal` paragraph format |
| `styles.h1_size` … `styles.h6_size` | `Heading 1` … `Heading 6` style font sizes |
| `styles.heading_space_before` / `heading_space_after` | `Heading 1` paragraph format (applied to H1–H6) |
| `styles.bullet_indent_cm` / `bullet_space_after` | `List Bullet` (fallback `List Number`) indent / spacing |
| `styles.code_font` / `styles.code_size` | `Code Block` style font name / size — compared only when the style exists in the docx (`_extracted.has_code_style`); otherwise the yaml value is render-only |
| `styles.heading_color` | Not extracted (any color allowed in source) — set in YAML, applied at render |
| `page.size` / `orientation` | First section page dimensions (A4/Letter within 0.15cm, else recorded in `_extracted`) |
| `page.margin_*_cm`, `page.header/footer_distance_cm` | First section margins / distances (cm, rounded 2dp) |
| `cover.*`, `header_footer.*`, `toc_levels` | Not extracted — YAML-configured only (defaults = old hardcoded standard) |
| `_extracted.has_header` / `header_text` | Any section header: any text or image |
| `_extracted.header_has_image` | Any drawing/picture element in a header |
| `_extracted.has_footer` / `footer_text` | Any section footer text |
| `_extracted.logo_saved` | `assets/logo.<ext>` bóc từ ảnh header (rỗng nếu không có ảnh) |
| `header.logo_path` | Fact: `assets/logo.<ext>` extracted from the first header image (empty when no image); validate checks file existence only. Whether to USE it is a user-approved param, not a guess |
| `content.txt` | Not a param — raw dump (paragraphs with sizes, tables, header/footer text, image list) for the agent's purpose reading in `commands/import.md` §5 |

Style-level means: style definitions are compared, individual text runs are
ignored (a single odd run never counts as LỆCH). A docx attribute that was
never set explicitly (inherited theme default) never conflicts with the
yaml — at render the yaml wins, and `--validate` reports `(dùng YAML)`.
Only two explicit, differing values count as LỆCH. Document identity fields
(`company_name`, `solution_name`, `document_name`, ...) live in the yaml
params and are applied at export time. The agent proposes their values by
reading `content.txt` and understanding the template's purpose (free-form
inference with cited evidence); if the template is empty/generic (< 3
meaningful text blocks, no tables, no header/footer text), the agent must
propose 2–3 likely purposes and ask the user (purpose + needed info +
optional sample file) — never invent a purpose.

## 10. Placeholders (`{{name}}` / `[[name]]`)

Token syntax (both accepted): `{{ten_du_an}}`, `[[ngay_ky]]` — name matches
`[A-Za-z0-9_.-]+`, optional inner spaces. Detection scans body + tables +
headers/footers at `--import` (raw list in `_extracted.placeholders_found`);
the agent presents each for user confirmation and only confirmed entries land
in yaml `placeholders:` (`<tên>.value` + `<tên>.description`).

Fill priority at export: `--param name=value` (one-shot, not saved) >
`placeholders.<name>.value` (non-empty) > top-level yaml scalar of the same
name (e.g. `{{company_name}}` → `company_name`). Tokens without value stay
intact and abort the export with the missing-name list (exit 2) — the agent
asks the user to map/input, then reruns with `--param` or saves via `--update`.

Scope notes: the template governs its own header/footer (kept, linked into
content pages; generated chrome only when the template has none), so
header/footer tokens persist with filled values. Tokens living only in the
sample body disappear at export (body is replaced by rendered content).
`Code Block` paragraphs are never scanned nor substituted (literal `{{ }}`
in code samples).
