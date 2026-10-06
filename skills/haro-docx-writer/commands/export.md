# Export (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --export:<id>`. Do not act from memory: read every step first.
> **Ground rules:** template values are ground truth (resolved local-first).
> NEVER hand-craft `.docx` — ALWAYS call `scripts/build_docx.py` with
> `--template-id`.

## Command `/haro-docx-writer --export:<id> <file hoặc đường dẫn file>`

Renders the chosen input file to `.docx` using template `<id>`.

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --export:<id> <input> [-o out.docx]`.
  Id glued with `:` — e.g. `--export:congty-a docs/sad.md`.
- `<id>` — required. Unknown id → STOP with
  `LỖI: không tìm thấy mẫu '<id>'.` + hint `/haro-docx-writer --list`.
- `<input>` — required path: `.md`, `.txt`, or `.pdf`. It is the
  user-mentioned source — accept any user-mentioned file of these types.
- `-o / --output` — optional. Default:
  `.haro-docx-writer/output/<basename>-<id>-<YYYYMMDD-HHmm>.docx`.

### 2. Resolve template (ground truth, then ask)

The script resolves `--template-id` itself (local wins over global),
loading the template's `template.yaml` as `--config` and its
`template.docx` (styles only — content/headers stripped) as `--base-template`.
Headings render H1–H6, TOC follows `toc_levels`, page geometry/cover/header
sizes all come from the template. Missing company/solution/document
fields → ask the user for the missing values (SHORT picker/free-text,
allow skip → uses `(Chưa xác định)`), then apply via
`/haro-docx-writer --update:<id>` BEFORE exporting (never export with guessed names).
Also surface any params still at defaults (user skipped the purpose review
at `--import`) and offer to fill them first.

Logo: `header.logo_path` — if the file doesn't exist, continue WITHOUT logo
(leave the left header cell empty) and note it in the final summary. Never
web-search a logo.

### 3. Validate input by extension

- `.md` / `.txt` → native path.
- `.pdf` → the script attempts text extraction via `pypdf`. If `pypdf` is not
  installed or the PDF has no extractable text (scanned), STOP with message:
  `PDF này không trích xuất được chữ (file scan/ảnh). Hãy cung cấp bản .md/.txt.`
- Anything else (`.docx`, `.xlsx`, ...) → refuse with supported-type message:
  `Định dạng chưa hỗ trợ. Hãy dùng .md / .txt / .pdf.`
  A `.docx` the user wants as STYLE is a `--import:<id>` source, not an input.

### 4. Run the generator (the only way to produce .docx)

```bash
python skills/haro-docx-writer/scripts/build_docx.py \
  --input <input> --output <out.docx> \
  --template-id <id> --project-root .
```

- Run from the project root so relative paths resolve.
- On script failure: show stderr verbatim + one-line hint, do NOT retry with a
  different hand-rolled method.

### 5. Verify + report (SHORT)

1. Confirm the output file exists and opens (size > 0).
2. Report 5 lines max: output path, input source, template `<id>` + scope
   (local/global), reminder:
   `Mở file → chuột phải vào Mục lục → Update Field để hiện menu danh mục.`

### Examples

```text
/haro-docx-writer --export:congty-a docs/sad.md
/haro-docx-writer --export:congty-a specs/auth.txt -o dist/auth-spec.docx
/haro-docx-writer --export:congty-a "tài liệu/yêu cầu.pdf" -o dist/yeucau.docx
```
