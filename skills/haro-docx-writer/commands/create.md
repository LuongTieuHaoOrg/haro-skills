# Create (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --create:<id>`. Do not act from memory: read every step first.
> **Ground rules:** NEVER hand-craft `template.yaml` — the generator script
> creates it. NEVER overwrite an existing id silently. Reply to the user in
> Vietnamese with full diacritics.

## Command `/haro-docx-writer --create:<id> <file.docx hoặc đường dẫn>`

Registers a user-supplied `.docx` file as a new named template.

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --create:<id> <path>` — the id is glued to the flag
  with `:` (no space). Example: `--create:congty-a DieuLe.docx`.
- `<id>`: lowercase, 2–41 chars, `[a-z0-9-_]` (spaces become `-`).
  Invalid id → STOP with the rule + one valid example. Never auto-rename.
- `<path>`: required, must exist, must end in `.docx`. Missing/unreadable/
  non-docx → STOP with `LỖI: ...` + expected usage. A `.md/.txt/.pdf` here
  is a user error — those are `--export` inputs, not template sources.

### 2. Ask scope: local or global (always ask, never default silently)

Single picker call (picker tool when available, otherwise numbered list):

- `local` — `<project>/.haro-docx-writer/templates/<id>/` (dùng riêng cho dự án).
- `global` — `~/.haro-docx-writer/templates/<id>/` (dùng chung mọi dự án).

Also ask `tên mẫu` (free-text, default = id) and `mô tả` (free-text,
allow skip → `""`).

### 3. Duplicate check (before any copy)

The generator script enforces this, but check first to give the friendly
message: if `<id>` already exists in the chosen scope → STOP with:

```text
Id '<id>' đã tồn tại ở <local|global>. Dùng /haro-docx-writer --view:<id> để xem
hoặc /haro-docx-writer --update:<id> <nội dung> để sửa — không ghi đè.
```

If it exists only in the OTHER scope → warn one line
(`Lưu ý: id này đã có ở <scope kia>; bản mới sẽ...`) and ask confirm
before continuing. Resolution order is local-first.

### 4. Copy + extract (the only way to create a template)

Run from the project root:

```bash
python skills/haro-docx-writer/scripts/extract_template.py \
  --source <path> --id <id> --location <local|global> \
  --project-root . --name "<tên mẫu>" --description "<mô tả>"
```

- The script copies `<path>` → `.../<id>/template.docx`, extracts any header
  image → `.../<id>/assets/logo.<ext>`, generates `.../<id>/template.yaml`
  (meta + style/page params extracted style-level from the .docx merged over
  `templates/config.yaml` defaults — content params stay at defaults), and
  writes `.../<id>/content.txt` (machine dump of the .docx text/tables/
  headers/footers/images for the agent to read).
- The script NEVER guesses purpose or content values. Purpose understanding
  is the agent's job in step 5 below.
- Exit 3 = duplicate (relay the message, do not retry). Other failures:
  show stderr verbatim + one-line hint, do NOT hand-create the yaml.

### 5. Read the template's purpose + propose params (mandatory, agent does it)

Skill focus: unifying STYLE of output documents. Understanding the purpose
tells the agent which information the template should carry to make future
content creation convenient.

1. Read `.../<id>/content.txt` fully (plus the yaml style block for context).
2. **Case A — template has discernible content:** state in chat, in Vietnamese:
   - (a) *Mục đích mẫu* — 1–2 free-form sentences inferred from the content,
     each claim cited (`tiêu đề "..."`, `bảng ...`, `header ...`). Never force
     it into a fixed category.
   - (b) *Đề xuất thông số* — table `trường | giá trị thấy trong mẫu | nguồn | còn thiếu cần hỏi`:
     propose only fields that directly serve future content creation
     (company, logo, signers, version, ...). Mark fields the template implies
     but doesn't contain as `còn thiếu cần hỏi`.
3. **Case B — empty/generic template** (hard rule: fewer than 3 meaningful
   text blocks AND no tables AND no header/footer text): NEVER invent a
   purpose. Propose 2–3 likely purposes inferred from remaining traces
   (e.g. logo + formal font → báo cáo/đề xuất; bare Heading styles → tài
   liệu kỹ thuật...) and ask the user: (1) chốt mục đích — pick or describe,
   (2) mẫu cần mang thông tin nào, (3) có file nội dung mẫu không
   (optional path).
4. User approves per row (giữ/sửa/bỏ, free-text edits allowed). Apply approved
   rows via the `--update:<id>` workflow (`update_template.py --set`, or yaml
   edit + push) in the same session.
5. Ask: `Giữ nguyên hay chỉnh sửa thông số style?` (keep / edit list).
   Style edits now → apply via `--update:<id>` workflow (same session).
6. Close with: `Xem lại: /haro-docx-writer --view:<id> | Kiểm tra: /haro-docx-writer --validate:<id> | Xuất thử: /haro-docx-writer --export:<id> <file.md>`.

### Examples

```text
/haro-docx-writer --create:congty-a DieuLe-CongTyA.docx
/haro-docx-writer --create:nhadaut-x "tai lieu/mau-trinhky.docx"
```
