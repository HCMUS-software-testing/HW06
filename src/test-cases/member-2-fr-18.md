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
| 1 | TC-FR18-AI-001 | VALID | Admin token và 200/list response là oracle rõ; cần fixture có tối thiểu hai users để chứng minh phạm vi toàn hệ thống. |
| 2 | TC-FR18-AI-002 | VALID | User token phải bị RBAC chặn 403, đồng thời xác nhận không lộ dữ liệu đơn hàng. |
| 3 | TC-FR18-AI-003 | VALID | Thiếu Authorization phải trả 401 trước khi truy cập tài nguyên. |
| 4 | TC-FR18-AI-004 | VALID | JWT sai cấu trúc/chữ ký phải bị từ chối bằng 401. |
| 5 | TC-FR18-AI-005 | VALID | JWT hết hạn phải trả 401; dùng token đã kiểm soát được thời gian hết hạn. |
| 6 | TC-FR18-AI-006 | INCOMPLETE | Thiếu precondition order đang `pending`; nếu ID=1 ở trạng thái khác thì 200 không còn đúng. |
| 7 | TC-FR18-AI-007 | VALID | User thường gọi mutation admin phải 403 và trạng thái DB phải không đổi. |
| 8 | TC-FR18-AI-008 | VALID | Thiếu token trên endpoint mutation phải 401, không phát sinh side effect. |
| 9 | TC-FR18-AI-009 | VALID | Bearer rỗng là credentials không hợp lệ; phải bị từ chối 401. |
| 10 | TC-FR18-AI-010 | INCOMPLETE | Query `status` chưa được xác nhận trong endpoint §6.2; cần contract filter, enum và behavior với status invalid. |
| 11 | TC-FR18-AI-011 | VALID | Role phải lấy từ JWT/server-side identity, không tin custom header; 403 là oracle phù hợp. |
| 12 | TC-FR18-AI-012 | INVALID | Gọi endpoint list nhưng kỳ vọng chi tiết một đơn; phải có `GET /api/admin/orders/:id` nếu đặc tả cung cấp. |
| 13 | TC-FR18-AI-013 | INCOMPLETE | API JSON không tự render HTML; cần fixture address chứa payload và kiểm UI/DOM sink riêng. |
| 14 | TC-FR18-AI-014 | INVALID | Endpoint `/api/users/me` nằm ngoài FR-18 và cho phép 200/400 không tạo oracle xác định; chuyển thành test riêng của user profile. |
| 15 | TC-FR18-AI-015 | VALID | Payload JWT sửa nhưng không re-sign phải fail verification và trả 401. |
| 16 | TC-FR18-AI-016 | INCOMPLETE | `shipping` chỉ hợp lệ từ `confirmed`; cần state precondition và kiểm transition. |
| 17 | TC-FR18-AI-017 | INCOMPLETE | `delivered` chỉ hợp lệ từ `shipping`; cần fixture và side-effect audit. |
| 18 | TC-FR18-AI-018 | INCOMPLETE | Cancel chỉ hợp lệ từ state cho phép; cần nêu `pending`/`confirmed` và quy tắc hoàn kho. |
| 19 | TC-FR18-AI-019 | VALID | Có precondition pending và transition hợp lệ với response 200 rõ ràng. |
| 20 | TC-FR18-AI-020 | VALID | Có precondition confirmed và transition hợp lệ với response 200 rõ ràng. |
| 21 | TC-FR18-AI-021 | VALID | Có precondition shipping và transition hợp lệ với response 200 rõ ràng. |
| 22 | TC-FR18-AI-022 | VALID | Pending sang canceled là transition hợp lệ theo FR-10. |
| 23 | TC-FR18-AI-023 | VALID | Confirmed sang canceled là transition hợp lệ theo FR-10. |
| 24 | TC-FR18-AI-024 | VALID | Final state delivered không được quay về pending; 400 và trạng thái không đổi là oracle đúng. |
| 25 | TC-FR18-AI-025 | VALID | Delivered không được chuyển sang canceled; cần kiểm không hoàn kho/không đổi dữ liệu. |
| 26 | TC-FR18-AI-026 | VALID | Canceled là final state, không được chuyển shipping. |
| 27 | TC-FR18-AI-027 | VALID | Canceled là final state, không được chuyển delivered. |
| 28 | TC-FR18-AI-028 | VALID | Delivered sang confirmed vi phạm state machine; 400 là phù hợp. |
| 29 | TC-FR18-AI-029 | VALID | Value ngoài enum phải bị validation từ chối và không đổi state. |
| 30 | TC-FR18-AI-030 | VALID | Order không tồn tại với ID hợp lệ phải trả 404. |
| 31 | TC-FR18-AI-031 | INCOMPLETE | Chấp nhận cả 400/404 khiến assertion mơ hồ; chốt contract validation path ID. |
| 32 | TC-FR18-AI-032 | INCOMPLETE | Tương tự TC31: phải chọn một status code và error schema cụ thể. |
| 33 | TC-FR18-AI-033 | VALID | ID 0 không tồn tại có 404 rõ ràng, nếu router nhận ID số. |
| 34 | TC-FR18-AI-034 | VALID | Missing required `status` phải trả 400 trước state transition. |
| 35 | TC-FR18-AI-035 | INCOMPLETE | `null` hợp lệ JSON còn malformed JSON là lỗi parser khác; tách thành hai test có Content-Type/oracle riêng. |

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-HUMAN-001 | Người dùng thường tự hủy đơn hàng khi đơn đã ở trạng thái `shipping` | State Violation (FR-10) | 1. Đơn hàng ID=1 đang ở trạng thái `shipping`<br>2. User gọi `PUT /api/orders/1/cancel` với User Token | Trả về 400 Bad Request ("Không thể tự hủy đơn hàng đang giao"), chỉ Admin mới được xử lý | AI thường bỏ qua quy tắc phân quyền theo trạng thái đơn (User chỉ được hủy khi `pending`/`confirmed`) |
| TC-FR18-HUMAN-002 | Chuyển trạng thái trùng lặp (Idempotent Status Update) | State Machine Edge | Admin gửi 2 request liên tiếp `PUT /api/admin/orders/1/status` với body `{"status": "confirmed"}` khi đơn đã là `confirmed` | Trả về 200 OK (Idempotent success), trạng thái giữ nguyên `confirmed`, không báo lỗi crash | AI ít khi kiểm thử tính lặp lại (Idempotence) của API cập nhật trạng thái với cùng giá trị |
| TC-FR18-HUMAN-003 | Khôi phục tồn kho sản phẩm khi Admin hủy đơn từ `confirmed` sang `canceled` | Inventory Restoration | 1. Đơn hàng có SP A (quantity=2) ở trạng thái `confirmed`<br>2. Admin gọi `PUT /api/admin/orders/1/status` body `{"status": "canceled"}` | Đơn chuyển sang `canceled`, số lượng tồn kho SP A tự động tăng thêm +2 trong CSDL | AI sinh testcase đơn lẻ kiểm tra HTTP response mà không verify side-effect trên cơ sở dữ liệu |
| TC-FR18-HUMAN-004 | Thử nghiệm Mass Assignment qua endpoint cập nhật status | Security / Mass Assignment | Admin gửi `PUT /api/admin/orders/1/status` với body `{"status": "confirmed", "total_amount": 0, "user_id": 999}` | Chỉ trường `status` được cập nhật sang `confirmed`, các trường `total_amount` và `user_id` không bị ghi đè | AI bỏ sót kiểm thử lỗi Mass Assignment làm thay đổi dữ liệu nhạy cảm qua API partial update |
| TC-FR18-HUMAN-005 | Phân quyền Admin đa chi nhánh / Multi-tenant Admin IDOR | Security / Authorization | Admin thuộc Store A gọi `PUT /api/admin/orders/99/status` cập nhật đơn hàng thuộc Store B | Trả về 403 Forbidden / 404 Not Found, không cho phép Admin vùng này can thiệp đơn của vùng khác | AI mặc định coi tất cả Admin có quyền ngang nhau mà không tính tới phân quyền mô hình Multi-tenant |

### Bổ sung human-designed: Privilege Escalation và rollback khi lỗi hệ thống

| Test Case ID | Tên kịch bản | Loại | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-HUMAN-006 | Sửa `role` qua profile rồi dùng token cũ gọi status API | Privilege Escalation | User gửi `PUT /api/users/me` với `{"role":"admin"}`; dùng chính access token cũ gọi `PUT /api/admin/orders/1/status` | Profile không đổi role; request status trả 403; state order không đổi | AI hay kiểm từng endpoint tách rời, bỏ qua chuỗi escalation có token/session thật. |
| TC-FR18-HUMAN-007 | Forged JWT `role=admin` ký bằng `alg:none` hoặc đổi `kid` | JWT Authorization | Tạo token payload user nhưng `role=admin`, bỏ chữ ký hoặc dùng key-id không hợp lệ; gọi status API | Trả 401, không chấp nhận thuật toán/key ngoài allowlist, không đổi state | AI thường chỉ kiểm token hỏng chung chung, không kiểm bypass xác minh JWT cụ thể. |
| TC-FR18-HUMAN-008 | Mass assignment kết hợp user token và role/body giả mạo | Privilege Escalation | User token gọi status API với `{"status":"confirmed","role":"admin","isAdmin":true}` | Trả 403 trước body processing; không có field nào được ghi | AI có thể chỉ kiểm role header hoặc body riêng lẻ, bỏ thứ tự authz-before-mutation. |
| TC-FR18-HUMAN-009 | Rollback khi lỗi sau cập nhật state nhưng trước khi ghi audit/event | Transaction Rollback | Dùng fault injection làm audit-log/message publish lỗi khi admin chuyển `confirmed` → `shipping`; đọc lại order và tồn kho | Response 5xx phù hợp; order, audit/event và side effect cùng rollback, không state "shipping" một phần | AI thường giả định request hoàn tất nguyên tử và không đưa failure injection vào oracle. |
| TC-FR18-HUMAN-010 | Rollback khi hủy đơn gặp lỗi hoàn kho | Transaction Rollback | Đơn `confirmed` có quantity=2; inject lỗi DB khi tăng tồn kho trong `→ canceled`; đọc lại order/kho | Không chuyển canceled nếu hoàn kho thất bại; status và stock giữ giá trị trước transaction | AI hay chỉ kiểm HTTP status, không kiểm atomicity giữa state order và inventory. |
