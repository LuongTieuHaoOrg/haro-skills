# Config (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx config`. Do not act from memory.
> **Ground rules:** this command OWNS `.haro-docx/config.yaml`. Never write it
> from any other command. Reply to the user in Vietnamese with full diacritics.

## Command `/haro-docx config`

Teaches the user where configuration lives, then scaffolds it. The skill reads
config on every export — it never asks the same company info twice.

### 1. Explain (chat, SHORT — 6 lines max, Vietnamese with diacritics)

- File cấu hình: `.haro-docx/config.yaml` (project root, per-project).
- Thư mục mẫu: `.haro-docx/` (*.docx templates riêng của dự án) + skill's
  `resources/templates/` (mẫu đi kèm). `--template` picker reads both.
- Output mặc định: `.haro-docx/output/`.
- Muốn dùng mẫu của công ty: copy file `.docx` của công ty vào `.haro-docx/`
  rồi tham chiếu bằng tên khi gọi `export --template <tên>`.

### 2. Scaffold on confirm

1. If `.haro-docx/config.yaml` is missing → copy from
   `skills/haro-docx/templates/config.yaml`, then ask for the 6 fields below
   (free-text each, allow skip):
   - `company_name` (footer/header dòng 2, trang bìa)
   - `solution_name` (footer phải, trang bìa)
   - `document_name` (header dòng 1)
   - `document_title` (trang bìa, mặc định = document_name)
   - `header.logo_path` (đường dẫn logo, để trống = không logo)
   - `authors` / `reviewers` / `approvers` (bảng phụ trách)
2. If it exists → show current values as a compact table + ask per-row
   keep/change (never overwrite silently).
3. Ensure `.haro-docx/output/` and `.haro-docx/*.docx` lookup dir exist.
4. Close with: `Xong. Chạy /haro-docx export <file> để xuất thử.`

### 3. Template management (tell, don't auto-run)

- Thêm mẫu: `copy congty.docx .haro-docx/` (ghi đè phải xác nhận).
- Xem mẫu: `/haro-docx export --template` (picker).
- Mẫu mặc định của skill: `skills/haro-docx/resources/templates/` — chỉ đọc,
  không sửa trực tiếp; muốn biến thể thì copy ra `.haro-docx/`.

### Example

```
/haro-docx config
```
