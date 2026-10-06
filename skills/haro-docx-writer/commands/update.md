# Update (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --update:<id>`. Do not act from memory: read every step first.
> **Ground rules:** NEVER hand-edit `template.docx` binary with tricks —
> visual changes go through `scripts/update_template.py`. NEVER interpret a
> vague request freely.

## Command `/haro-docx-writer --update:<id> <nội dung>`

Updates a template's params (yaml) and, when the request touches visual
style, patches the `.docx` file to match.

### 1. Parse args (no guessing)

- Syntax: `/haro-docx-writer --update:<id> <nội dung>` — id glued with `:`,
  then free-text content. Example:
  `/haro-docx-writer --update:congty-a đổi company thành CTY X, H1 lên 15`.
- Unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx-writer --list`. Resolve with:
  `python skills/haro-docx-writer/scripts/template_store.py --project-root . resolve <id>`
  (local wins over global — show the winning scope).

### 2. Vague-content gate (mandatory — ask back, never guess)

If `<nội dung>` is empty or vague (`làm đẹp hơn`, `sửa giúp anh`,
`cập nhật đi`, single word with no target, ...), STOP and ask back with a
concrete picker (multiple choice allowed):

- Đổi thông tin công ty / giải pháp / tài liệu (company/solution/document)
- Đổi font / cỡ chữ (body/H1/H2/H3/code)
- Đổi logo header
- Đổi tên / mô tả mẫu
- Khác (gõ yêu cầu cụ thể: trường nào → giá trị nào)

Only proceed once at least one `trường → giá trị` pair is explicit.

### 3. Apply (yaml first, then push visual into docx)

Mappable `--set` keys for `scripts/update_template.py`:

- Text/meta: `name`, `description`, `company_name`, `solution_name`,
  `document_name`, `document_title`, `version`, `date`, `status`,
  `header.logo_path`, `toc_levels` (`1-N`, e.g. `1-6`).
- Styles: `styles.body_font`, `styles.body_size`, `styles.h1_size` …
  `styles.h6_size`, `styles.body_line_spacing`, `styles.body_space_before`,
  `styles.body_space_after`, `styles.heading_space_before`,
  `styles.heading_space_after`, `styles.bullet_indent_cm`,
  `styles.bullet_space_after`, `styles.code_font`, `styles.code_size`,
  `styles.heading_color` (hex, e.g. `000000`).
- Page: `page.size` (`A4`/`Letter`), `page.orientation`
  (`portrait`/`landscape`), `page.margin_top/bottom/left/right_cm`,
  `page.header/footer_distance_cm`.
- Cover/header-footer sizes: `cover.title/solution/company/note_size`,
  `header_footer.doc_name/company/page/solution_size` (export-time only —
  yaml saved, nothing pushed into the .docx).
- Lists (`authors`, `reviewers`, `approvers`): comma-separated.
- Units: numeric values accept bare numbers (legacy meaning) or strings with
  units — `"15pt"`, `"2cm"`, `"25mm"`, `"1in"` (auto-converted). Examples:
  `--set styles.h1_size="15pt"`, `--set page.margin_left_cm="25mm"`.
  Bad units are refused with a clear error.
- Anything outside this list (cover layout, header/footer structure,
  TOC behavior beyond levels) → explain it is fixed by `shared/docx-style.md`
  + script; offer the closest supported alternative instead of improvising.

Run from the project root (repeatable `--set`, dot-paths):

```bash
python skills/haro-docx-writer/scripts/update_template.py \
  --id <id> --project-root . \
  --set company_name="CTY X" --set styles.h1_size=15
```

- The script saves `template.yaml`, bumps `updated_at`, and pushes
  style-level keys (fonts, sizes, spacing, bullet, page geometry) into
  `template.docx`. Pure text/meta/cover-size requests may pass
  `--no-apply-visual` (docx untouched).
- If the user already hand-edited `template.yaml` themselves, skip `--set`
  for those keys and run with no `--set` to only refresh `updated_at` +
  push current yaml styles into the docx.

### 4. Confirm + close (SHORT)

1. Show the before → after diff per key (from script output).
2. Run `/haro-docx-writer --validate:<id>` workflow next (or its script) and
   report `KHỚP/LỆCH` summary — never skip validation after an update.
3. Close with file paths (yaml + docx).

### Examples

```text
/haro-docx-writer --update:congty-a đổi company_name thành CÔNG TY X, version 2.0
/haro-docx-writer --update:congty-a styles.h1_size=15, styles.body_font="Times New Roman"
/haro-docx-writer --update:congty-a đổi logo header thành assets/logo-moi.png
```
