# Hệ thống Quản lý Kho — Đặc tả Kỹ thuật (bản mẫu)

Tài liệu mẫu dùng để thử `/haro-docx --export:<id>`. Chạy thử:

```bash
python skills/haro-docx/scripts/build_docx.py \
  --input skills/haro-docx/templates/sample-input.md \
  --output .haro-docx/output/mau-sad.docx \
  --template-id <id> --project-root .
```

## 1. Tổng quan

Hệ thống quản lý kho (WMS-lite) phục vụ 3 kho, khoảng 50 người dùng đồng thời.
Mục tiêu: tồn kho chính xác theo thời gian thực, truy vết xuất/nhập.

## 2. Yêu cầu chức năng

- N-01 — Quản lý danh mục hàng hoá (mã SKU, đơn vị, hạn dùng).
- N-02 — Nhập kho theo phiếu, kiểm tra lệch số lượng.

### 2.1. Quy tắc nghiệp vụ

| Mã    | Quy tắc                  | Ghi chú              |
|-------|--------------------------|----------------------|
| BR-01 | Không xuất âm tồn kho    | Chặn ở tầng service  |
| BR-02 | FIFO theo lô hạn dùng    | Cảnh báo trước 30 ngày |

## 3. Thiết kế kỹ thuật

Stack: Python + PostgreSQL. Xác thực JWT, phân quyền theo vai trò.

```
POST /api/v1/goods-receipts
Authorization: Bearer <token>
```

---

Phiên bản mẫu — thay nội dung này bằng specs thật của dự án.
