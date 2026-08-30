# Báo Cáo Lỗi Phát Hiện Được (Bug Report — Member 1)

**Người thực hiện:** Lâm Hữu Khánh (23127205)  
**Phạm vi:** FR-02 (Đăng nhập & Khóa TK), FR-07 (Giỏ hàng), FR-15 (Quản lý sản phẩm CRUD)  

---

## Danh Sách Lỗi Phát Hiện

| Bug ID | API liên quan | Tiêu đề lỗi | Mức độ | Trạng thái GitHub Issue |
|:---:|---|---|:---:|:---:|
| `BUG-FR02-01` | `POST /api/login` | Bộ đếm `login_attempts` tăng 2 đơn vị mỗi lần sai thay vì 1 đơn vị | High | Đã log Issue #1 |
| `BUG-FR02-02` | `POST /api/login` | Thời gian khóa tài khoản là 180s (3 phút) thay vì 30s theo đặc tả | Medium | Đã log Issue #2 |
| `BUG-FR07-01` | `POST /api/cart` | Backend không có kiểm tra số lượng `quantity <= 0` hoặc số âm | High | Đã log Issue #3 |
| `BUG-FR07-02` | `/api/cart` | Thiếu hoàn toàn API Cập nhật số lượng (`PUT`) và Xóa item (`DELETE`) | Critical | Đã log Issue #4 |
| `BUG-FR15-01` | `POST /api/products` | Thiếu middleware kiểm tra phân quyền Admin (`authenticateToken`) | Critical | Đã log Issue #5 |
| `BUG-FR15-02` | `GET /api/products/:id` | Ép kiểu `price` sang String ở các sản phẩm có ID chẵn | Medium | Đã log Issue #6 |
| `BUG-FR15-03` | `POST /api/products` | Cho phép tạo sản phẩm với giá âm và giá bằng 0 | High | Đã log Issue #7 |
