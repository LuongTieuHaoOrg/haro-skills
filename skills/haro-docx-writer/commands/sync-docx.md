# Sync-docx (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --sync-docx:<id>`. Do not act from memory: read every
> step first.
> **Ground rules:** this command pushes YAML into DOCX — it never edits yaml
> values. NEVER hand-edit `template.docx` — the updater script does it.

## Command `/haro-docx-writer --sync-docx:<id>`

Pushes the template's yaml config (styles/page) into its `template.docx`.
Run it after hand-editing `template.yaml` (or after `--update` with
`--no-apply-visual`).

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --sync-docx:<id>` — id glued with `:`. Extra
  tokens → warn and ignore.
- Unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx-writer --list`.

### 2. Sync (yaml wins, no yaml edits)

Run from the project root with NO `--set` (any `--set` here belongs to
`--update`, not sync):

```bash
python skills/haro-docx-writer/scripts/update_template.py \
  --id <id> --project-root .
```

- The script keeps every yaml value, bumps `updated_at`, and pushes
  styles/page into `template.docx`. Pure yaml→docx, one direction.
- On failure: show stderr verbatim + one-line hint, do NOT hand-edit.

### 3. Confirm + close (SHORT)

1. Show the pushed list from script output (`Normal.*`, `Heading *`,
   `List *`, `page=...`).
2. Run the `--validate:<id>` workflow next — expect all KHỚP.
3. Close with file paths (yaml + docx).

### Example

```text
/haro-docx-writer --sync-docx:congty-a
```
