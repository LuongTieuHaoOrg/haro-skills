# List (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx --list`. Do not act from memory: read every step first.
> **Ground rules:** this command is read-only — never create, copy, or edit
> any file. Reply to the user in Vietnamese with full diacritics.

## Command `/haro-docx --list`

Lists every registered template: id, name, description, storage location
(local = project, global = home dir), creation time, update time.

### 1. Parse args (no guessing)

- Exact command is `/haro-docx --list` with no extra tokens. Extra tokens
  after `--list` → warn `Lệnh --list không nhận thêm tham số.` and ignore them.

### 2. Scan registries (the only source of truth)

Run from the project root:

```bash
python skills/haro-docx/scripts/template_store.py --project-root . list
```

- Never hand-scan directories or guess ids — the script output wins.
- Local scope = `<project>/.haro-docx/templates/<id>/`.
  Global scope = `~/.haro-docx/templates/<id>/`.

### 3. Render (Vietnamese with diacritics)

Render one table with exactly these columns:

| id mẫu | tên mẫu | mô tả | vị trí lưu | thời gian tạo | thời gian cập nhật |
|--------|---------|-------|------------|---------------|--------------------|

- `vị trí lưu` shows `local` or `global` only.
- Empty registry → print `Chưa có mẫu nào.` + one line:
  `Tạo mẫu đầu tiên: /haro-docx --create:<id> <file.docx>`.
- 6 lines max after the table: totals (`N mẫu local, M mẫu global`) +
  next-action hint (`Xem chi tiết: /haro-docx --view:<id>`).

### Example

```text
/haro-docx --list
```
