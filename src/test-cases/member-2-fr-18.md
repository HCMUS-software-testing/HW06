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

### Authoritative audit and final AI inventory

> **Fixture contract cho mọi mutation NEWMAN:** tạo order mới qua checkout, capture ID động, đưa order tới đúng `starting state`, snapshot toàn bộ order, rồi mới gọi admin status API. Accepted transition: 200 JSON và đúng final state. Rejected/auth/parser request: status nêu cụ thể, JSON error và snapshot order không đổi. Không dùng ID cố định `1`. Malformed JSON và JSON `null` được tách thành AI-010 và AI-035.

| ID | Verdict | Technical reason | Final correction | Execution class |
| --- | --- | --- | --- | --- |
| TC-FR18-AI-001 | VALID | Admin list có direct RBAC/list oracle. | Tạo orders cho hai fresh users; admin GET 200 JSON array và list chứa cả hai captured IDs. | NEWMAN |
| TC-FR18-AI-002 | VALID | User role phải bị chặn ở admin list. | Fresh user token GET; 403 JSON và body không lộ captured admin-order fixtures. | NEWMAN |
| TC-FR18-AI-003 | VALID | Missing Authorization có 401 oracle. | GET không Authorization; 401 JSON, không order data. | NEWMAN |
| TC-FR18-AI-004 | VALID | Invalid JWT phải fail authentication. | GET với malformed/signed-invalid token; 401 JSON, không order data. | NEWMAN |
| TC-FR18-AI-005 | VALID | Expired token là deterministic auth boundary. | GET với controlled expired admin token; 401 JSON, không order data. | NEWMAN |
| TC-FR18-AI-006 | INCOMPLETE | Original không thiết lập starting state. | Fresh order `pending`; admin PUT `confirmed`; 200 và final state exactly `confirmed`. | NEWMAN |
| TC-FR18-AI-007 | VALID | User mutation phải 403 và không side effect. | Fresh order `pending`; user token PUT `confirmed`; 403, full order snapshot unchanged. | NEWMAN |
| TC-FR18-AI-008 | VALID | Missing auth phải bị chặn trước mutation. | Fresh `pending` order; no Authorization PUT; 401, snapshot unchanged. | NEWMAN |
| TC-FR18-AI-009 | VALID | Empty bearer là invalid credentials. | Fresh `pending` order; empty bearer PUT; 401, snapshot unchanged. | NEWMAN |
| TC-FR18-AI-010 | INVALID | Original filter query không có trong verified §6.2 contract. | Replacement/split partner: fresh `pending` order; malformed JSON body với correct content type; 400 parser error, snapshot unchanged. | NEWMAN |
| TC-FR18-AI-011 | VALID | Custom role header không được override JWT role. | Fresh `pending` order exists; user token plus `X-Role: admin` GET; 403 và không order data. | NEWMAN |
| TC-FR18-AI-012 | INVALID | Original gọi list nhưng kỳ vọng undocumented detail endpoint. | Replacement: admin GET list 200; locate captured ID in array and verify its required order fields without calling detail route. | NEWMAN |
| TC-FR18-AI-013 | INCOMPLETE | JSON cannot prove admin DOM escaping. | Seed order address with unique HTML/event sentinel; admin browser list renders it as text, no executable node/event, one order row for captured ID. | BROWSER-MANUAL |
| TC-FR18-AI-014 | INVALID | Profile endpoint nằm ngoài FR-18 và original cho 200/400. | Privilege chain: user attempts profile `role=admin`, then same token GET admin list; assertion on GET is 403, role remains user, no order data. | NEWMAN |
| TC-FR18-AI-015 | VALID | Tampered payload with old signature must fail verification. | GET with user JWT payload changed to admin but not re-signed; 401 JSON, no order data. | NEWMAN |
| TC-FR18-AI-016 | INCOMPLETE | Shipping only valid from confirmed. | Fresh order advanced to `confirmed`; PUT `shipping`; 200 and final state `shipping`. | NEWMAN |
| TC-FR18-AI-017 | INCOMPLETE | Delivered only valid from shipping. | Fresh order advanced to `shipping`; PUT `delivered`; 200 and final state `delivered`. | NEWMAN |
| TC-FR18-AI-018 | INCOMPLETE | Cancel starting state was unspecified and stock restoration is undocumented. | Fresh order `pending`; PUT `canceled`; 200 and final state `canceled`; no stock oracle is added. | NEWMAN |
| TC-FR18-AI-019 | VALID | Pending to confirmed is allowed. | Fresh `pending` order; PUT `confirmed`; 200 and exact final state `confirmed`. | NEWMAN |
| TC-FR18-AI-020 | VALID | Confirmed to shipping is allowed. | Fresh order advanced to `confirmed`; PUT `shipping`; 200 and exact final state `shipping`. | NEWMAN |
| TC-FR18-AI-021 | VALID | Shipping to delivered is allowed. | Fresh order advanced to `shipping`; PUT `delivered`; 200 and exact final state `delivered`. | NEWMAN |
| TC-FR18-AI-022 | VALID | Pending to canceled is allowed. | Fresh `pending` order; PUT `canceled`; 200 and exact final state `canceled`. | NEWMAN |
| TC-FR18-AI-023 | VALID | Confirmed to canceled is allowed. | Fresh order advanced to `confirmed`; PUT `canceled`; 200 and exact final state `canceled`. | NEWMAN |
| TC-FR18-AI-024 | VALID | Delivered is final. | Fresh order advanced to `delivered`; PUT `pending`; 400 JSON and full snapshot remains `delivered`. | NEWMAN |
| TC-FR18-AI-025 | VALID | Delivered cannot transition to canceled. | Fresh `delivered` order; PUT `canceled`; 400 and full snapshot unchanged. | NEWMAN |
| TC-FR18-AI-026 | VALID | Canceled is final. | Fresh `canceled` order; PUT `shipping`; 400 and full snapshot unchanged. | NEWMAN |
| TC-FR18-AI-027 | VALID | Canceled cannot transition to delivered. | Fresh `canceled` order; PUT `delivered`; 400 and full snapshot unchanged. | NEWMAN |
| TC-FR18-AI-028 | VALID | Delivered to confirmed violates state machine. | Fresh `delivered` order; PUT `confirmed`; 400 and full snapshot unchanged. | NEWMAN |
| TC-FR18-AI-029 | VALID | Unknown enum must be rejected before mutation. | Fresh `pending` order; PUT `unknown_status_xyz`; 400 and full snapshot unchanged. | NEWMAN |
| TC-FR18-AI-030 | VALID | Valid numeric missing ID has 404 oracle. | Reserve/calculate nonexistent positive ID; PUT `confirmed`; 404 JSON and all control orders unchanged. | NEWMAN |
| TC-FR18-AI-031 | INCOMPLETE | Original 400/404 is ambiguous and path validation is unspecified. | PUT ID `-1`; assert contract-safe invariant status not 500, JSON error and known control order snapshot unchanged; record observed status later. | NEWMAN |
| TC-FR18-AI-032 | INCOMPLETE | Original 400/404 is ambiguous and path coercion unspecified. | PUT ID `abc`; assert status not 500, JSON error and control order unchanged; record observed status later. | NEWMAN |
| TC-FR18-AI-033 | VALID | ID 0 is a deterministic nonexistent resource. | PUT ID `0`; 404 JSON and all control orders unchanged. | NEWMAN |
| TC-FR18-AI-034 | VALID | Missing required status must be rejected. | Fresh `pending` order; body `{}`; 400 JSON and full snapshot unchanged. | NEWMAN |
| TC-FR18-AI-035 | INCOMPLETE | Original conflated valid JSON null with malformed JSON. | JSON-null half only: fresh `pending` order; body `null` with JSON content type; 400 JSON and full snapshot unchanged. Malformed half is AI-010. | NEWMAN |

---

## 2. Authoritative human-designed inventory (10 cases)

| ID | Final corrected scenario and deterministic oracle | Execution class | Why AI missed it |
| --- | --- | --- | --- |
| TC-FR18-HUMAN-001 | Original user-cancel route is outside selected scope. Replacement: fresh order advanced to `shipping`; user token calls admin status PUT `canceled`; 403 and full snapshot remains `shipping`. | NEWMAN | Combines state and authorization-before-mutation. |
| TC-FR18-HUMAN-002 | Fresh order advanced to `confirmed`; admin requests `confirmed` again. Same-state edge is not an allowed transition, so 400 and full snapshot remains `confirmed`. | NEWMAN | AI assumed idempotence without state-machine evidence. |
| TC-FR18-HUMAN-003 | Inventory restoration on cancellation cannot be observed: public contract has no stock field/mutation endpoint. Keep design, claim no run/result. | EXCLUDED | Needs inventory side-effect visibility. |
| TC-FR18-HUMAN-004 | Fresh `pending` order; admin PUT includes `status=confirmed`, `total_amount=0`, `user_id=999`; 200, status becomes confirmed, every non-status field equals pre-snapshot. | NEWMAN | Requires mass-assignment differential snapshot. |
| TC-FR18-HUMAN-005 | Multi-tenant stores/admin scopes are absent from verified contract; do not invent Store A/B fixture or 403/404 result. | EXCLUDED | Assumed tenancy model not present in SUT contract. |
| TC-FR18-HUMAN-006 | User attempts profile role assignment; verify role remains user, then same token calls admin PUT on fresh `pending` order; 403 and order snapshot unchanged. | NEWMAN | Cross-endpoint escalation chain. |
| TC-FR18-HUMAN-007 | For fresh `pending` order, send both `alg:none` and invalid-`kid` forged admin JWT probes; each 401 and order snapshot unchanged. One assertion aggregates both controlled probes. | NEWMAN | Requires concrete JWT bypass variants. |
| TC-FR18-HUMAN-008 | User token calls admin PUT with `status=confirmed`, `role=admin`, `isAdmin=true`; 403 occurs before body mutation and full `pending` snapshot is unchanged. | NEWMAN | Verifies authorization ordering, not only status code. |
| TC-FR18-HUMAN-009 | With a test-only hook, fail audit/event write after requested `confirmed` to `shipping`; request fails and order/event snapshots remain pre-transaction. No public hook exists. | FAULT-INJECTION | Atomic rollback needs deterministic failure injection. |
| TC-FR18-HUMAN-010 | With a test-only hook, fail inventory restoration during `confirmed` to `canceled`; request fails and order/stock snapshots remain unchanged. No public stock/fault hook exists. | FAULT-INJECTION | Cross-resource rollback is not black-box triggerable. |
