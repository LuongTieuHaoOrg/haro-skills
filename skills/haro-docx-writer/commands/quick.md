# Quick (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer <file>` — a bare file argument with NO flag. Do not act
> from memory: read every step first.
> **Ground rules:** template values are ground truth (picked by the user,
> resolved local-first). NEVER hand-craft `.docx` — ALWAYS call
> `scripts/build_docx.py`.

## Command `/haro-docx-writer <file hoặc đường dẫn file>`

Quick export: the user gives only an input file; the skill loads existing
templates for the user to pick one, then renders.

### 1. Parse args (no guessing)

- Applies ONLY when the first token does NOT start with `--` — treat it as
  `<input>` path. Flag tokens route per the `SKILL.md` table, never here.
- `<input>` — required: `.md`, `.txt`, or `.pdf` (the user-mentioned source).
- `.docx` input → STOP (a `.docx` is a template SOURCE, not an export input):
  tell the user to register it first —
  `/haro-docx-writer --import:<id> <file.docx>` — then quick-export from
  `.md` / `.txt` / `.pdf`.
- Anything else (`.xlsx`, ...) → refuse:
  `Định dạng chưa hỗ trợ. Hãy dùng .md / .txt / .pdf.`

### 2. Load templates for the user to pick (mandatory)

Run from the project root:

```bash
python skills/haro-docx-writer/scripts/template_store.py --project-root . list
```

- **No templates at all → STOP with error, do nothing else:**
  `Chưa có mẫu nào. Hãy tạo mẫu trước: /haro-docx-writer --import:<id> <file.docx>.`
  Point at the basic default shipped with the skill
  (`skills/haro-docx-writer/templates/default-template.docx`) as the fastest
  first template, then STOP and wait.
- **Otherwise → single picker call** (picker tool when available, otherwise
  numbered list) with one entry per template: `<id> — <tên mẫu> (<local|global>)`.
  The user picks exactly one — that `<id>` is used. NEVER auto-pick, NEVER guess.

### 3. Export (same engine as `--export`)

```bash
python skills/haro-docx-writer/scripts/build_docx.py \
  --input <input> --output <out.docx> \
  --template-id <id> --project-root .
```

- Default output: `.haro-docx-writer/output/<basename>-<id>-<YYYYMMDD-HHmm>.docx`.
- Missing company/solution/document fields → ask the user (SHORT picker/free-text,
  allow skip → `(Chưa xác định)`), apply via `--update:<id>` BEFORE exporting.
- Logo file missing → continue WITHOUT logo, note it in the summary. Never
  web-search a logo.
- On script failure: show stderr verbatim + one-line hint, do NOT hand-roll.

### 4. Verify + report (SHORT)

1. Confirm the output file exists and opens (size > 0).
2. Report 5 lines max: output path, input source, template `<id>` + scope
   (local/global) the user picked, reminder:
   `Mở file → chuột phải vào Mục lục → Update Field để hiện menu danh mục.`

### Example

```text
/haro-docx-writer docs/sad.md
```
