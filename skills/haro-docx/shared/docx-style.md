# DOCX Style — Enterprise Standard (Haro Docx, normative)

> `scripts/build_docx.py` implements this file. The agent must NOT restyle
> by hand — change this file plus the script instead.

## 1. Font and color (defaults, whole document)

- Single typeface for all text: `Times New Roman`. Single ink: black `000000`.
  No other font or color anywhere (including header, footer, cover, tables,
  TOC).
- H1: 14pt, bold. H2: 13pt, bold. H3: 12pt, bold.
- Body: 12pt, regular.
- Code / endpoints / parameters: `Consolas` 11pt inside a light-grey frame,
  original English kept as-is (the skill only formats, never translates).
- Emphasis via bold or italic only — never a different font or color.
- Fonts are forced at run level on export: every text run carries its font
  directly, so a Word template theme (`--base-template`) can never override
  headings or body text.

## 2. Alignment and spacing

- Body text justified on both sides. Headings left-aligned. The cover page is
  fully centered.
- No horizontal separator rules (no horizontal lines, no paragraph borders).
  Chapters are separated by headings plus whitespace (space before/after). A
  `---` line in markdown becomes just a blank paragraph.

## 3. Cover page (page 1, no header/footer, centered)

Centered, from top: optional logo (max 3cm) → `DOCUMENT_TITLE` (24pt bold
black) → `SOLUTION_NAME` (14pt) → `COMPANY_NAME` (12pt) → meta table
(Phiên bản / Ngày / Tác giả / Trạng thái) → note
`Tài liệu lưu hành nội bộ.` The cover ends with a page break.

## 4. Control pages (page 2–3, no header/footer)

- `Lịch sử thay đổi` — 4-column table (Phiên bản / Ngày / Nội dung / Người sửa),
  header row bold on the single light-grey fill. Seeds one row from config
  (`version`, `date`, `Danh mục ban đầu`, `authors[0]`).
- `Người phụ trách` — 3-column table (Vai trò / Họ tên / Chữ ký) with rows
  Biên soạn (authors), Kiểm tra (reviewers), Phê duyệt (approvers).
- Every table uses `Table Grid` (full borders), repeating header row, no
  merged cells, no fill color other than the header row's light grey.

## 5. TOC page ("Mục lục")

- Heading `Mục lục` plus a real Word `TOC \o "1-3" \h \z \u` field paragraph so
  Word fills in page numbers on open. Followed by an instructional italic line:
  `Mở file → chuột phải → Update Field để hiện menu danh mục.`
- Ends with a page break; body sections start after it.

## 6. Header (content pages only — cover/control/TOC have none)

Two-column borderless table: left cell (30%) = logo image if configured
(max height 1.2cm), else empty; right cell (70%) right-aligned with 2 lines:
line 1 = `DOCUMENT_NAME` bold 9pt, line 2 = `COMPANY_NAME` regular 8pt.
All black, Times New Roman. Header distance 1.27cm.

## 7. Footer (content pages only)

Two-column borderless table: left = `Trang <PAGE> / <NUMPAGES>` field codes
(8pt); right cell right-aligned = `SOLUTION_NAME` (8pt italic).
All black, Times New Roman. Footer distance 1.27cm.

## 8. Body mapping (md/txt → docx)

| Source | Output |
|--------|--------|
| `#` / `##` / `###` | Heading 1/2/3, left-aligned (deeper levels → Heading 3) |
| plain paragraph | Normal, justified |
| `- ` / `* ` / `1.` | List Bullet / List Number, left-aligned |
| `\| a \| b \|` | Table Grid with full borders, first row = bold + light-grey fill |
| fenced ` ``` ` | Code style (Consolas 11pt, grey background, English kept as-is) |
| `![alt](path)` | Centered figure + caption right below (`Hình N: alt`, italic 11pt). Image files must live under `assets/`, never base64 embeds; an unresolvable path becomes an italic placeholder line instead |
| `---` | Blank paragraph (whitespace), NEVER a page break or a rule line |

PDF input is plain extracted text: a blank line starts a new paragraph, and
ALL-CAPS or numbered (`1.`, `1.1`) lines are heuristically promoted to headings.
