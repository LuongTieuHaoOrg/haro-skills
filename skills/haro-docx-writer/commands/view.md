# View (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --view:<id>`. Do not act from memory: read every step first.
> **Ground rules:** this command is read-only — never create, edit, or
> delete anything.

## Command `/haro-docx-writer --view:<id>`

Shows a template's configuration for review: file paths + full params.

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --view:<id>` — id glued with `:`. Extra tokens →
  warn and ignore.
- Unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx-writer --list`.

### 2. Resolve (local wins over global)

```bash
python skills/haro-docx-writer/scripts/template_store.py --project-root . resolve <id>
```

Show exactly: `id`, `vị trí` (local/global), `đường dẫn file yaml`,
`đường dẫn file mẫu (.docx)`.

### 3. Display full config

Read the resolved `template.yaml` fully and display it grouped:

1. **Meta:** id / tên / mô tả / vị trí / tạo lúc / cập nhật lúc / file nguồn.
2. **Thông tin tài liệu:** company / solution / document / version / date /
   status / authors / reviewers / approvers.
3. **Header & logo:** `header.logo_path` (+ file có tồn tại không).
4. **Styles:** body font/size/line-spacing/spacing, H1–H6, heading spacing,
   bullet indent/spacing, code, heading color.
5. **Trang:** size/orientation, 4 margins, header/footer distances.
6. **Cover/header-footer/TOC:** `cover.*`, `header_footer.*`, `toc_levels`.
7. **Nội dung gốc của mẫu:** point to `.../<id>/content.txt` (machine dump
   of the docx text/tables/headers) when the user wants to see what the
   template contains. Purpose discussion belongs to `--import`, not here —
   never present guesses as facts.

Never truncate silently — if long, keep the grouping and summarize lists.
Do not interpret or validate here; for mismatch checks point to
`/haro-docx-writer --validate:<id>`, for changes to `/haro-docx-writer --update:<id>`.

### Example

```text
/haro-docx-writer --view:congty-a
```
