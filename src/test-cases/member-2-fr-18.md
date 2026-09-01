# Test Cases & Audit - FR-18: Quản lý đơn hàng Admin

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoints:**
- `GET /api/admin/orders` — Xem danh sách toàn bộ đơn hàng (api_specification.md §6.2)
- `PUT /api/admin/orders/:id/status` — Cập nhật trạng thái đơn hàng (api_specification.md §6.2)

**Header bắt buộc:** `Authorization: Bearer <adminToken>`, `X-Student-Id: 23127075`  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` §6.2 & `eshop-sut/README.md` FR-10, FR-12, FR-18, SEC-02, SEC-03, SEC-04, SEC-06

---

## 1. Danh Sách Test Cases AI Sinh (35 Test Cases) & Kiểm Toán Audit

### Batch 1: Quyền truy cập Admin & Phân quyền RBAC (18 test cases)

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

### Batch 2: Máy trạng thái đơn hàng (FR-10 State Machine) & Path Parameters (17 test cases)

> **Phạm vi kiểm thử:**
> - **Chuyển trạng thái hợp lệ (FR-10):** `pending` -> `confirmed`, `confirmed` -> `shipping`, `shipping` -> `delivered`, `pending` -> `canceled`, `confirmed` -> `canceled`.
> - **Chuyển trạng thái KHÔNG hợp lệ / Final State Violation (FR-10):** `delivered` -> `pending`, `delivered` -> `canceled`, `canceled` -> `shipping`, `canceled` -> `delivered`, `delivered` -> `confirmed`, giá trị status không hợp lệ (`"unknown_status"`).
> - **Path Parameter & Validation:** `order_id` không tồn tại (404), `order_id` âm (400/404), `order_id` chuỗi (400/404), `order_id` = 0 (404), thiếu trường `status` trong body (400), payload `null` (400).

| STT | Test Case Name | Method | Endpoint | Request Header / Body | Expected Status | Expected Body / Response Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| 19 | Chuyển trạng thái hợp lệ: `pending` -> `confirmed` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 200 OK | Đơn hàng từ `pending` chuyển sang `confirmed` thành công |
| 20 | Chuyển trạng thái hợp lệ: `confirmed` -> `shipping` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "shipping"}` | 200 OK | Đơn hàng từ `confirmed` chuyển sang `shipping` thành công |
| 21 | Chuyển trạng thái hợp lệ: `shipping` -> `delivered` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "delivered"}` | 200 OK | Đơn hàng từ `shipping` chuyển sang `delivered` thành công |
| 22 | Chuyển trạng thái hợp lệ: `pending` -> `canceled` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` | 200 OK | Đơn hàng từ `pending` hủy sang `canceled` thành công |
| 23 | Chuyển trạng thái hợp lệ: `confirmed` -> `canceled` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` | 200 OK | Đơn hàng từ `confirmed` hủy sang `canceled` thành công |
| 24 | Chuyển trạng thái KHÔNG hợp lệ: `delivered` -> `pending` (Final State Violation) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "pending"}` *(Đơn đang delivered)* | 400 Bad Request | Từ chối do `delivered` là trạng thái kết thúc (Final State FR-10) |
| 25 | Chuyển trạng thái KHÔNG hợp lệ: `delivered` -> `canceled` (Final State Violation) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` *(Đơn đang delivered)* | 400 Bad Request | Từ chối chuyển đổi trạng thái từ đơn đã giao thành công |
| 26 | Chuyển trạng thái KHÔNG hợp lệ: `canceled` -> `shipping` (Final State Violation) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "shipping"}` *(Đơn đang canceled)* | 400 Bad Request | Từ chối do `canceled` là trạng thái kết thúc (Final State FR-10) |
| 27 | Chuyển trạng thái KHÔNG hợp lệ: `canceled` -> `delivered` (Final State Violation) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "delivered"}` *(Đơn đang canceled)* | 400 Bad Request | Từ chối chuyển trạng thái đơn hàng đã bị hủy |
| 28 | Chuyển trạng thái quay ngược KHÔNG hợp lệ: `delivered` -> `confirmed` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` *(Đơn đang delivered)* | 400 Bad Request | Không cho phép chuyển ngược trạng thái từ delivered |
| 29 | Cập nhật giá trị `status` không nằm trong danh mục enum cho phép | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "unknown_status_xyz"}` | 400 Bad Request | Thông báo lỗi trạng thái không hợp lệ (chỉ nhận: pending, confirmed, shipping, delivered, canceled) |
| 30 | Cập nhật trạng thái cho `order_id` không tồn tại trong CSDL | PUT | `/api/admin/orders/9999999/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 404 Not Found | Thông báo lỗi không tìm thấy đơn hàng |
| 31 | Cập nhật trạng thái cho `order_id` mang giá trị âm (`:id = -1`) | PUT | `/api/admin/orders/-1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 400 Bad Request / 404 Not Found | Thông báo lỗi ID đơn hàng không hợp lệ |
| 32 | Cập nhật trạng thái cho `order_id` dạng chuỗi không phải số (`:id = abc`) | PUT | `/api/admin/orders/abc/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 400 Bad Request / 404 Not Found | Thông báo lỗi ID đơn hàng phải là kiểu số |
| 33 | Cập nhật trạng thái cho `order_id` bằng 0 (`:id = 0`) | PUT | `/api/admin/orders/0/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 404 Not Found | Thông báo lỗi đơn hàng không tồn tại |
| 34 | Body request thiếu trường `status` bắt buộc (`{}`) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{}` | 400 Bad Request | Thông báo lỗi trường `status` là bắt buộc |
| 35 | Body request dạng `null` hoặc sai cú pháp JSON | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `null` | 400 Bad Request | Thông báo lỗi payload không hợp lệ |

---

### Bảng Kiểm Toán Audit (35 Test Cases AI Sinh - FR-18)

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
| 19 | TC-FR18-AI-019 | [Manual by user] | [Manual by user] |
| 20 | TC-FR18-AI-020 | [Manual by user] | [Manual by user] |
| 21 | TC-FR18-AI-021 | [Manual by user] | [Manual by user] |
| 22 | TC-FR18-AI-022 | [Manual by user] | [Manual by user] |
| 23 | TC-FR18-AI-023 | [Manual by user] | [Manual by user] |
| 24 | TC-FR18-AI-024 | [Manual by user] | [Manual by user] |
| 25 | TC-FR18-AI-025 | [Manual by user] | [Manual by user] |
| 26 | TC-FR18-AI-026 | [Manual by user] | [Manual by user] |
| 27 | TC-FR18-AI-027 | [Manual by user] | [Manual by user] |
| 28 | TC-FR18-AI-028 | [Manual by user] | [Manual by user] |
| 29 | TC-FR18-AI-029 | [Manual by user] | [Manual by user] |
| 30 | TC-FR18-AI-030 | [Manual by user] | [Manual by user] |
| 31 | TC-FR18-AI-031 | [Manual by user] | [Manual by user] |
| 32 | TC-FR18-AI-032 | [Manual by user] | [Manual by user] |
| 33 | TC-FR18-AI-033 | [Manual by user] | [Manual by user] |
| 34 | TC-FR18-AI-034 | [Manual by user] | [Manual by user] |
| 35 | TC-FR18-AI-035 | [Manual by user] | [Manual by user] |

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-HUMAN-001 | Người dùng thường tự hủy đơn hàng khi đơn đã ở trạng thái `shipping` | State Violation (FR-10) | 1. Đơn hàng ID=1 đang ở trạng thái `shipping`<br>2. User gọi `PUT /api/orders/1/cancel` với User Token | Trả về 400 Bad Request ("Không thể tự hủy đơn hàng đang giao"), chỉ Admin mới được xử lý | AI thường bỏ qua quy tắc phân quyền theo trạng thái đơn (User chỉ được hủy khi `pending`/`confirmed`) |
| TC-FR18-HUMAN-002 | Chuyển trạng thái trùng lặp (Idempotent Status Update) | State Machine Edge | Admin gửi 2 request liên tiếp `PUT /api/admin/orders/1/status` với body `{"status": "confirmed"}` khi đơn đã là `confirmed` | Trả về 200 OK (Idempotent success), trạng thái giữ nguyên `confirmed`, không báo lỗi crash | AI ít khi kiểm thử tính lặp lại (Idempotence) của API cập nhật trạng thái với cùng giá trị |
| TC-FR18-HUMAN-003 | Khôi phục tồn kho sản phẩm khi Admin hủy đơn từ `confirmed` sang `canceled` | Inventory Restoration | 1. Đơn hàng có SP A (quantity=2) ở trạng thái `confirmed`<br>2. Admin gọi `PUT /api/admin/orders/1/status` body `{"status": "canceled"}` | Đơn chuyển sang `canceled`, số lượng tồn kho SP A tự động tăng thêm +2 trong CSDL | AI sinh testcase đơn lẻ kiểm tra HTTP response mà không verify side-effect trên cơ sở dữ liệu |
| TC-FR18-HUMAN-004 | Thử nghiệm Mass Assignment qua endpoint cập nhật status | Security / Mass Assignment | Admin gửi `PUT /api/admin/orders/1/status` với body `{"status": "confirmed", "total_amount": 0, "user_id": 999}` | Chỉ trường `status` được cập nhật sang `confirmed`, các trường `total_amount` và `user_id` không bị ghi đè | AI bỏ sót kiểm thử lỗi Mass Assignment làm thay đổi dữ liệu nhạy cảm qua API partial update |
| TC-FR18-HUMAN-005 | Phân quyền Admin đa chi nhánh / Multi-tenant Admin IDOR | Security / Authorization | Admin thuộc Store A gọi `PUT /api/admin/orders/99/status` cập nhật đơn hàng thuộc Store B | Trả về 403 Forbidden / 404 Not Found, không cho phép Admin vùng này can thiệp đơn của vùng khác | AI mặc định coi tất cả Admin có quyền ngang nhau mà không tính tới phân quyền mô hình Multi-tenant |
