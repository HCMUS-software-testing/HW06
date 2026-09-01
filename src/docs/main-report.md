# Báo Cáo Kiểm Thử API - HW06 (Member 2: Lê Trung Kiên - 23127075)

## 1. Tổng Quan Bài Làm
- **Họ và tên:** Lê Trung Kiên
- **MSSV:** 23127075
- **Các API phụ trách:**
  1. **FR-05 (Pool A):** Liệt kê và tìm kiếm sản phẩm
  2. **FR-08 (Pool B):** Thanh toán / tạo đơn hàng
  3. **FR-18 (Pool C):** Quản lý đơn hàng (Admin)

---

## 2. Chi Tiết Pipeline Cho Từng API

### 2.1. API 1: FR-05 - Liệt Kê Và Tìm Kiếm Sản Phẩm
- **Endpoint:** `GET /api/products`, `GET /api/products/search`
- **Quy trình AI Generation:**
- **Kết quả Audit (VALID / INVALID / INCOMPLETE):**
- **Test cases tự bổ sung (Human-designed):**
- **Kết quả thực thi Newman:**

### 2.2. API 2: FR-08 - Thanh Toán / Tạo Đơn Hàng
- **Endpoint:** `POST /api/orders/checkout`
- **Quy trình AI Generation:**
- **Kết quả Audit (VALID / INVALID / INCOMPLETE):**
- **Test cases tự bổ sung (Human-designed):**
- **Kết quả thực thi Newman:**

### 2.3. API 3: FR-18 - Quản Lý Đơn Hàng Admin
- **Endpoint:** `GET /api/admin/orders`, `PUT /api/admin/orders/{id}/status`
- **Quy trình AI Generation:**
- **Kết quả Audit (VALID / INVALID / INCOMPLETE):**
- **Test cases tự bổ sung (Human-designed):**
- **Kết quả thực thi Newman:**

---

## 3. Danh Sách Tính Năng Postman Đã Sử Dụng
- **Workspaces & Collections:** Tổ chức các API request theo nhóm tính năng.
- **Environment Variables:** Quản lý `baseUrl`, `authToken`, `adminToken`, `studentId`.
- **Pre-request Scripts:** Tự động gắn header `X-Student-Id: 23127075` vào mọi request.
- **Tests Scripts & Assertions:** Kiểm tra status code, response time, response schema validation (JSON Schema), và business logic fields.
- **Collection Runner & Data-Driven Testing:** Chạy lặp test suite với file dữ liệu CSV/JSON.

---

## 4. Báo Cáo Phát Hiện Lỗi (Bug Reporting Summary)
- Tóm tắt danh sách các lỗi thật tìm thấy trong SUT cho 3 API phụ trách.
