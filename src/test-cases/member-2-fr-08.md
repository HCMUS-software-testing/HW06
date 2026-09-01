# Test Cases & Audit - FR-08: Thanh toán / Tạo đơn hàng

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoint:** `POST /api/orders/checkout`  

## 1. Danh Sách Test Cases AI Sinh (>= 35 cases) & Kiểm Toán Audit

| Test Case ID | Tên kịch bản kiểm thử | Mô tả & Input parameters | Expected Result | Trạng thái Audit (VALID / INVALID / INCOMPLETE) | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- | --- | --- |
| TC-FR08-AI-001 | Checkout thành công với giỏ hàng hợp lệ | `POST /api/orders/checkout` với Auth Token & giỏ hàng có hàng | Returns 201 Created + order details | VALID | Test case hợp lệ |

*(Danh sách chi tiết 35 test cases do AI sinh sẽ được ghi đầy đủ tại đây)*

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR08-HUMAN-001 | Checkout khi giỏ hàng vừa bị rỗng ở tab khác | Race condition / State | `POST /api/orders/checkout` khi cart_items đã bị xóa | Returns 400 Bad Request ("Cart is empty") | AI bỏ sót race condition/thao tác đa phiên |
