# Test Cases & Audit - FR-05: Liệt kê và tìm kiếm sản phẩm

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoint:** `GET /api/products`, `GET /api/products/search`  

## 1. Danh Sách Test Cases AI Sinh (>= 35 cases) & Kiểm Toán Audit

| Test Case ID | Tên kịch bản kiểm thử | Mô tả & Input parameters | Expected Result | Trạng thái Audit (VALID / INVALID / INCOMPLETE) | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | Liệt kê danh sách sản phẩm mặc định | `GET /api/products` không truyền params | Returns 200 OK + danh sách sản phẩm phân trang mặc định | VALID | Test case hợp lệ |

*(Danh sách chi tiết 35 test cases do AI sinh sẽ được ghi đầy đủ tại đây)*

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR05-HUMAN-001 | SQL Injection trong query keyword | Security | `GET /api/products/search?q=' OR '1'='1` | Returns 400 Bad Request hoặc Sanitized query result | AI thiếu ngữ cảnh kiểm thử bảo mật injection |
