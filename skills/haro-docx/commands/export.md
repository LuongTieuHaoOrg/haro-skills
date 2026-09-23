# Export (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx export`. Do not act from memory: read every step first.
> **Ground rules:** config values are ground truth (see `commands/config.md`).
> NEVER hand-craft `.docx` — ALWAYS call `scripts/build_docx.py`. Reply to the
> user in Vietnamese with full diacritics.

## Command `/haro-docx export <input> [-o out.docx] [--template name]`

### 1. Parse args (no guessing)

- `<input>` — required path (except bare `--template` picker mode): `.md`,
  `.txt`, or `.pdf`. It is the user-mentioned source — accept any
  user-mentioned file of these types.
- `-o / --output` — optional. Default:
  `.haro-docx/output/<basename>-<YYYYMMDD-HHmm>.docx`.
- `--template` — optional:
  - `--template` with NO value → picker mode: list `resources/templates/*.docx`
    in the skill folder PLUS `*.docx` under `.haro-docx/` (user templates),
    let the user pick one, then STOP and wait for the real export call with
    the chosen name.
  - `--template <name>` → use that template's styles as the base (passed as
    `--base-template` to the script). Missing name = error listing available
    names, no fallback guessing.

### 2. Resolve config (ground truth, then ask)

1. Load `.haro-docx/config.yaml` if present, else `templates/config.yaml`
   defaults. Missing company/solution/document fields → ask the user for the
   missing values (SHORT picker/free-text, allow skip → uses `(Chưa xác định)`).
2. Logo: `header.logo_path` — if the file doesn't exist, continue WITHOUT logo
   (leave the left header cell empty) and note it in the final summary. Never
   web-search a logo.

### 3. Validate input by extension

- `.md` / `.txt` → native path.
- `.pdf` → the script attempts text extraction via `pypdf`. If `pypdf` is not
  installed or the PDF has no extractable text (scanned), STOP with message:
  `PDF này không trích xuất được chữ (file scan/ảnh). Hãy cung cấp bản .md/.txt.`
- Anything else (`.docx`, `.xlsx`, ...) → refuse with supported-type message:
  `Định dạng chưa hỗ trợ. Hãy dùng .md / .txt / .pdf.`
  A `.docx` the user wants as STYLE goes to `--template`, not `<input>`.

### 4. Run the generator (the only way to produce .docx)

```bash
python skills/haro-docx/scripts/build_docx.py \
  --input <input> --output <out.docx> \
  --config <resolved-config.yaml> \
  [--base-template <template.docx>]
```

- Run from the project root so relative paths resolve.
- On script failure: show stderr verbatim + one-line hint, do NOT retry with a
  different hand-rolled method.

### 5. Verify + report (SHORT, Vietnamese with diacritics)

1. Confirm the output file exists and opens (size > 0).
2. Report 5 lines max: output path, input source, template used (or `mặc định`),
   config source (`.haro-docx/config.yaml` vs `mặc định`), reminder:
   `Mở file → chuột phải vào Mục lục → Update Field để hiện menu danh mục.`

### Examples

```
/haro-docx export docs/sad.md
/haro-docx export specs/auth.txt -o dist/auth-spec.docx
/haro-docx export "tài liệu/yêu cầu.pdf" -o dist/yeucau.docx
/haro-docx export --template
/haro-docx export docs/sad.md --template congty-a
```
