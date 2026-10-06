# Validate (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --validate:<id>`. Do not act from memory: read every step first.
> **Ground rules:** this command REPORTS mismatches — it never fixes them
> by itself. Fixes go through `--update:<id>`. Reply to the user in
> Vietnamese with full diacritics.

## Command `/haro-docx-writer --validate:<id>`

Checks whether `template.yaml` and the real `template.docx` agree —
for cases where the user edited one of the two files with different params.

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --validate:<id>` — id glued with `:`. Extra tokens →
  warn and ignore.
- Unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx-writer --list`.

### 2. Run the checker (style-level only)

Run from the project root:

```bash
python skills/haro-docx-writer/scripts/validate_template.py --id <id> --project-root .
```

- Scope: `styles.*` (fonts, H1–H6 sizes, line/paragraph spacing, bullet
  indent/spacing, code, heading color is yaml-only) + `page.*` (size,
  orientation, 4 margins, header/footer distances) + header/footer presence
  recorded in `_extracted` + `header.logo_path` file existence (including
  `assets/logo.*` inside the template folder). Run-level oddities are ignored
  by design (no false positives) — see `shared/docx-style.md` §9.
- Exit 0 = all match; exit 1 = mismatches (normal case, not an error);
  exit 2 = broken template (missing yaml/docx/unreadable) — relay stderr.

### 3. Report (Vietnamese with diacritics)

1. Show header: id, scope, yaml path, docx path.
2. Render the `[KHỚP/LỆCH]` table from script output verbatim (one row per
   field: `yaml='...' | docx='...'`).
3. For each LỆCH row, state the direction explicitly:
   - User edited the `.docx` → update YAML to match (edit keys, or re-run
     extraction flow) — or run `--update:<id>` with the docx values.
   - User edited the `YAML` → run `/haro-docx-writer --update:<id> <nội dung>`
     to push styles into the `.docx`.
4. Never auto-fix. End with the two follow-ups:
   `Sửa yaml: /haro-docx-writer --update:<id> ... | Xuất thử: /haro-docx-writer --export:<id> <file.md>`.

### Example

```text
/haro-docx-writer --validate:congty-a
```
