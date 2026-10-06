# Sync-yaml (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --sync-yaml:<id>`. Do not act from memory: read every
> step first.
> **Ground rules:** this command pulls DOCX into YAML — the .docx wins and
> overwrites yaml styles/page with NO backup. NEVER hand-edit `template.yaml`
> to fake it — the sync script does it.

## Command `/haro-docx-writer --sync-yaml:<id>`

Re-extracts styles/page from `template.docx` into `template.yaml`. Run it
after hand-editing the `.docx` in Word (fonts, sizes, spacing, margins).

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --sync-yaml:<id>` — id glued with `:`. Extra
  tokens → warn and ignore.
- Unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx-writer --list`.

### 2. Sync (docx wins, no backup)

Run from the project root:

```bash
python skills/haro-docx-writer/scripts/sync_yaml.py \
  --id <id> --project-root .
```

- Overwrites ONLY `styles` + `page` (+ `_extracted` facts, `content.txt`,
  logo re-extract). Identity params, meta, `cover`/`header_footer`/
  `toc_levels` are YAML-owned and stay untouched.
- NO backup file is made — say so explicitly before running when the yaml
  holds values not present in the docx (check via `--validate:<id>` first
  if unsure).
- On failure: show stderr verbatim + one-line hint, do NOT hand-edit.

### 3. Confirm + close (SHORT)

1. Show the before → after diff per key from script output (these are exactly
   what the .docx imposed on the yaml).
2. Run the `--validate:<id>` workflow next — expect all KHỚP.
3. Close with file paths (yaml + docx).

### Example

```text
/haro-docx-writer --sync-yaml:congty-a
```
