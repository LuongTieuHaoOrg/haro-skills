# Delete (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx --delete:<id>`. Do not act from memory: read every step first.
> **Ground rules:** deletion is irreversible (no trash). NEVER delete without
> explicit confirm. Reply to the user in Vietnamese with full diacritics.

## Command `/haro-docx --delete:<id>`

Deletes a template folder (`template.yaml` + `template.docx`).

### 1. Parse args (no guessing)

- Syntax: `/haro-docx --delete:<id>` — id glued with `:`. No extra path
  argument. Extra tokens → warn and ignore.
- Unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx --list`.

### 2. Show what will be deleted

Resolve all scopes holding the id (local and global may both exist):

```bash
python skills/haro-docx/scripts/template_store.py --project-root . resolve <id>
```

plus `--list`-style meta (name/description/updated_at) for each scope hit.
If both scopes hold the id → picker: `local` / `global` / `cả hai` /
`hủy`. If one scope → that scope is the target (still needs confirm).

### 3. Explicit confirm (mandatory)

Ask for explicit confirmation naming the target, e.g.
`Gõ 'xoa <id> (<vị trí>)' để xác nhận, hoặc chọn Hủy.`
(or a confirm/cancel picker when available). No confirm → STOP, delete nothing.

### 4. Delete (whole folder only)

Delete the entire `.../templates/<id>/` directory (both `template.yaml`
and `template.docx` inside) for the confirmed scope(s) — never delete
single files, never touch the other scope, never touch
`.haro-docx/output/`. Then verify the folder is gone and report:

```text
Đã xóa mẫu '<id>' ở <local|global> (<đường dẫn thư mục>).
```

### Example

```text
/haro-docx --delete:congty-a
```
