# Test Cases & Audit - FR-18: Quản lý đơn hàng Admin

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoints:**
- `GET /api/admin/orders` — Xem danh sách toàn bộ đơn hàng (api_specification.md §6.2)
- `PUT /api/admin/orders/:id/status` — Cập nhật trạng thái đơn hàng (api_specification.md §6.2)

**Header bắt buộc:** `Authorization: Bearer <adminToken>`, `X-Student-Id: 23127075`  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` §6.2 & `eshop-sut/README.md` FR-10, FR-12, FR-18, SEC-02, SEC-03, SEC-04, SEC-06

---

## 1. Danh Sách Test Cases AI Sinh & Kiểm Toán Audit

### Batch 1: Quyền truy cập Admin & Phân quyền RBAC (18 test cases)

> **Phạm vi kiểm thử:**
> - **Quyền truy cập Admin hợp lệ:** Xem danh sách toàn bộ đơn hàng hệ thống với `adminToken` (`role='admin'`), cập nhật trạng thái đơn hàng (`pending` -> `confirmed` -> `shipping` -> `delivered` / `canceled`).
> - **Kiểm soát truy cập RBAC (SEC-03, SEC-04):** Truy cập bằng `userToken` (`role='user'`) -> 403 Forbidden; truy cập không có Token -> 401 Unauthorized; Token không hợp lệ/hết hạn/chữ ký bị sửa đổi -> 401 Unauthorized; giả mạo Header `X-Role: admin` -> 403 Forbidden; tự nâng quyền qua API profile -> 403/400.
> - **An toàn hiển thị (README FR-18):** Kiểm tra `shipping_address` chứa XSS payload được trả về an toàn.

| STT | Test Case Name | Method | Endpoint | Request Header / Body | Expected Status | Expected Body / Response Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Admin xem danh sách toàn bộ đơn hàng hệ thống | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | Trả về mảng JSON chứa tất cả đơn hàng của mọi người dùng trong hệ thống |
| 2 | User thường cố truy cập danh sách đơn hàng Admin (RBAC Violation) | GET | `/api/admin/orders` | Header: `Bearer <userToken>` (`role='user'`) | 403 Forbidden | Từ chối truy cập (SEC-03: API Admin phải kiểm tra `role='admin'`) |
| 3 | Truy cập danh sách đơn hàng Admin khi chưa đăng nhập | GET | `/api/admin/orders` | Header: *(Không gửi Authorization)* | 401 Unauthorized | Thông báo yêu cầu đăng nhập (SEC-02) |
| 4 | Truy cập danh sách đơn hàng Admin với Token không hợp lệ | GET | `/api/admin/orders` | Header: `Bearer invalid_token_123` | 401 Unauthorized | Từ chối do Token sai chữ ký hoặc cấu trúc |
| 5 | Truy cập danh sách đơn hàng Admin với Token đã hết hạn | GET | `/api/admin/orders` | Header: `Bearer <expiredAdminToken>` | 401 Unauthorized | Thông báo phiên đăng nhập Admin đã hết hạn |
| 6 | Admin cập nhật trạng thái đơn hàng sang `confirmed` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 200 OK | Cập nhật trạng thái đơn hàng ID=1 sang `confirmed` thành công |
| 7 | User thường cố cập nhật trạng thái đơn hàng qua API Admin (Privilege Escalation) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <userToken>`<br>Body: `{"status": "confirmed"}` | 403 Forbidden | Từ chối truy cập, chỉ Admin mới có quyền đổi trạng thái đơn hàng |
| 8 | Cập nhật trạng thái đơn hàng Admin không có Token | PUT | `/api/admin/orders/1/status` | Header: *(Không gửi Authorization)*<br>Body: `{"status": "confirmed"}` | 401 Unauthorized | Yêu cầu xác thực tài khoản Admin |
| 9 | Cập nhật trạng thái đơn hàng với Bearer Token rỗng | PUT | `/api/admin/orders/1/status` | Header: `Bearer `<br>Body: `{"status": "confirmed"}` | 401 Unauthorized | Từ chối truy cập do Token rỗng |
| 10 | Admin xem danh sách đơn hàng lọc theo trạng thái `pending` | GET | `/api/admin/orders` | Header: `Bearer <adminToken>`<br>Query: `?status=pending` | 200 OK | Mảng JSON chứa các đơn hàng ở trạng thái `pending` |
| 11 | User thường cố gửi Header giả mạo `X-Role: admin` | GET | `/api/admin/orders` | Header: `Bearer <userToken>`, `X-Role: admin` | 403 Forbidden | Backend chỉ đọc role từ JWT claims, không tin tưởng custom header |
| 12 | Admin xem chi tiết đơn hàng của người dùng bất kỳ | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | Hiển thị đầy đủ thông tin đơn hàng và thông tin người đặt |
| 13 | Kiểm tra an toàn hiển thị địa chỉ giao hàng (Safety Output) | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | Trường `shipping_address` có chứa ký tự HTML/XSS được escape an toàn (README FR-18) |
| 14 | User thường cố tự nâng quyền bằng cách sửa `role` trong profile | PUT | `/api/users/me` | Header: `Bearer <userToken>`<br>Body: `{"role": "admin"}` | 200 OK / 400 | Thuộc tính `role` giữ nguyên là `user`, không thể tự nâng quyền thành Admin (SEC-06) |
| 15 | Gửi JWT Token bị sửa đổi Payload (`role='admin'`) nhưng giữ nguyên chữ ký cũ | GET | `/api/admin/orders` | Header: `Bearer <tamperedJWT>` | 401 Unauthorized | Phát hiện chữ ký không khớp với payload và từ chối truy cập |
| 16 | Admin cập nhật trạng thái đơn hàng sang `shipping` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "shipping"}` | 200 OK | Trạng thái đơn hàng chuyển sang `shipping` |
| 17 | Admin cập nhật trạng thái đơn hàng sang `delivered` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "delivered"}` | 200 OK | Trạng thái đơn hàng chuyển sang `delivered` (Final State) |
| 18 | Admin cập nhật trạng thái đơn hàng sang `canceled` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` | 200 OK | Trạng thái đơn hàng chuyển sang `canceled` (Final State) |

---

### Bảng Kiểm Toán Audit — Batch 1 (18 Test Cases)

| STT | Test Case ID | Trạng thái Audit | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- |
| 1 | TC-FR18-AI-001 | [Manual by user] | [Manual by user] |
| 2 | TC-FR18-AI-002 | [Manual by user] | [Manual by user] |
| 3 | TC-FR18-AI-003 | [Manual by user] | [Manual by user] |
| 4 | TC-FR18-AI-004 | [Manual by user] | [Manual by user] |
| 5 | TC-FR18-AI-005 | [Manual by user] | [Manual by user] |
| 6 | TC-FR18-AI-006 | [Manual by user] | [Manual by user] |
| 7 | TC-FR18-AI-007 | [Manual by user] | [Manual by user] |
| 8 | TC-FR18-AI-008 | [Manual by user] | [Manual by user] |
| 9 | TC-FR18-AI-009 | [Manual by user] | [Manual by user] |
| 10 | TC-FR18-AI-010 | [Manual by user] | [Manual by user] |
| 11 | TC-FR18-AI-011 | [Manual by user] | [Manual by user] |
| 12 | TC-FR18-AI-012 | [Manual by user] | [Manual by user] |
| 13 | TC-FR18-AI-013 | [Manual by user] | [Manual by user] |
| 14 | TC-FR18-AI-014 | [Manual by user] | [Manual by user] |
| 15 | TC-FR18-AI-015 | [Manual by user] | [Manual by user] |
| 16 | TC-FR18-AI-016 | [Manual by user] | [Manual by user] |
| 17 | TC-FR18-AI-017 | [Manual by user] | [Manual by user] |
| 18 | TC-FR18-AI-018 | [Manual by user] | [Manual by user] |

---

*(Batch 2: Máy trạng thái đơn hàng & IDOR Status Update — 17 test cases sẽ được bổ sung ở prompt tiếp theo)*

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| *(Sẽ được bổ sung sau khi hoàn thành kiểm toán audit batch 1 + batch 2)* | | | | | |
