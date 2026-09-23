# resources/templates — Style templates (.docx)

- Bỏ file `.docx` mẫu của công ty vào đây (bản đi kèm) hoặc vào `.haro-docx/`
  (bản riêng của dự án).
- `/haro-docx export --template` (picker) đọc cả hai nơi.
- `/haro-docx export ... --template <tên>` dùng styles của file đó làm nền
  (truyền `--base-template` cho script). Không sửa trực tiếp file trong này —
  muốn biến thể thì copy ra `.haro-docx/`.
- Hiện tại chưa có mẫu kèm sẵn: script tự dùng style mặc định trong
  `shared/docx-style.md` (Times New Roman đen), vẫn đạt chuẩn trình ký.
