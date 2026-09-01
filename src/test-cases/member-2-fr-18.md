# Test Cases & Audit - FR-18: Quản lý đơn hàng Admin

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoint:** `GET /api/admin/orders`, `PUT /api/admin/orders/{id}/status`  

## 1. Danh Sách Test Cases AI Sinh (>= 35 cases) & Kiểm Toán Audit

| Test Case ID | Tên kịch bản kiểm thử | Mô tả & Input parameters | Expected Result | Trạng thái Audit (VALID / INVALID / INCOMPLETE) | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-AI-001 | Admin xem danh sách đơn hàng | `GET /api/admin/orders` với Admin Token | Returns 200 OK + danh sách tất cả đơn hàng | VALID | Test case hợp lệ |

*(Danh sách chi tiết 35 test cases do AI sinh sẽ được ghi đầy đủ tại đây)*

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-HUMAN-001 | User thường cố truy cập Admin orders (Bảo mật Privilege Escalation) | Security / RBAC | `GET /api/admin/orders` với User Token | Returns 403 Forbidden | AI không giả định đúng vai trò phân quyền RBAC |
