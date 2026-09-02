# Test Cases & Audit - FR-08: Thanh toán / Tạo đơn hàng (Checkout)

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoint:** `POST /api/checkout` (api_specification.md §4.3)  
**Header bắt buộc:** `Authorization: Bearer <userToken>`, `X-Student-Id: 23127075`  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` §4.3 & `eshop-sut/README.md` FR-08, FR-09, FR-10, SEC-02, SEC-03, SEC-04

---

## 1. Danh Sách Test Cases AI Sinh (35 Test Cases) & Kiểm Toán Audit

### Batch 1: Nghiệp vụ Thanh toán, Giỏ hàng & Mã giảm giá (18 test cases)

| STT | Test Case Name | Method | Endpoint | Request Header / Body | Expected Status | Expected Body / Response Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Checkout thành công với địa chỉ giao hàng hợp lệ | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi, TP.HCM"}` | 200 OK | Trả về JSON object chứa `order_id` (hoặc `id`), `status`: "pending", `total_amount`: 200000 |
| 2 | Checkout khi giỏ hàng rỗng (Cart is empty) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 0, "shipping_address": "123 Le Loi, TP.HCM"}` | 400 Bad Request | Thông báo lỗi giỏ hàng rỗng, không tạo đơn |
| 3 | Checkout khi số lượng sản phẩm vượt quá tồn kho (Out of Stock) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 500000, "shipping_address": "123 Le Loi, TP.HCM"}` | 400 Bad Request / 409 Conflict | Thông báo lỗi sản phẩm vượt quá số lượng trong kho |
| 4 | Checkout với địa chỉ giao hàng rỗng (Empty String) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": ""}` | 400 Bad Request | Thông báo lỗi địa chỉ giao hàng không được để trống |
| 5 | Checkout với địa chỉ giao hàng chỉ chứa khoảng trắng | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "   "}` | 400 Bad Request | Thông báo lỗi địa chỉ giao hàng không hợp lệ |
| 6 | Checkout với địa chỉ giao hàng thiếu tên đường / chi tiết | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "TP.HCM"}` | 400 Bad Request / 200 OK | Kiểm tra địa chỉ có đủ thông tin giao hàng |
| 7 | Checkout với số điện thoại giao hàng sai định dạng | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "phone": "12345"}` | 400 Bad Request | Thông báo lỗi số điện thoại không hợp lệ (phải từ 10-11 số, bắt đầu bằng 0) |
| 8 | Checkout với địa chỉ giao hàng quá dài (> 500 ký tự) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "aaaa..." (500+ chars)}` | 400 Bad Request | Server từ chối địa chỉ vượt quá độ dài tối đa |
| 9 | Kiểm tra chống gian lận giá trị `total_amount` từ Client | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 1000, "shipping_address": "123 Le Loi, TP.HCM"}` *(Giỏ hàng thực tế 200,000đ)* | 200 OK | Backend tự động tính lại tổng tiền 200,000đ theo giỏ hàng thực tế; không dùng giá trị 1,000đ của Client |
| 10 | Checkout áp dụng mã giảm giá hợp lệ theo phần trăm (`SAVE10`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 450000, "shipping_address": "123 Le Loi", "coupon_code": "SAVE10"}` | 200 OK | Đơn hàng áp dụng giảm 10% trên tổng đơn 500,000đ, số tiền cuối cùng = 450,000đ |
| 11 | Checkout áp dụng mã giảm giá cố định hợp lệ (`BIGBUY`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 450000, "shipping_address": "123 Le Loi", "coupon_code": "BIGBUY"}` | 200 OK | Đơn hàng áp dụng giảm 50,000đ trên đơn 500,000đ, số tiền cuối cùng = 450,000đ |
| 12 | Checkout với mã giảm giá đã hết hạn (`EXPIRED`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 500000, "shipping_address": "123 Le Loi", "coupon_code": "EXPIRED"}` | 400 Bad Request | Thông báo lỗi mã giảm giá đã hết hạn sử dụng (C2) |
| 13 | Checkout với mã giảm giá không đủ giá trị đơn hàng tối thiểu | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "coupon_code": "BIGBUY"}` *(Đơn 200k < min 500k)* | 400 Bad Request | Thông báo lỗi chưa đạt giá trị đơn hàng tối thiểu để dùng mã (C3) |
| 14 | Checkout với mã giảm giá đã dùng hết số lần cho phép (`max_uses_per_user`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 400000, "shipping_address": "123 Le Loi", "coupon_code": "SAVE10"}` | 400 Bad Request | Thông báo lỗi bạn đã dùng hết số lần cho phép của mã giảm giá này (C5) |
| 15 | Checkout với mã giảm giá không tồn tại trong CSDL | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "coupon_code": "INVALID999"}` | 400 Bad Request / 404 Not Found | Thông báo lỗi mã giảm giá không tồn tại (C1) |
| 16 | Kiểm tra tự động xóa giỏ hàng sau khi checkout thành công | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Sau khi checkout thành công, gọi `GET /api/cart` trả về mảng giỏ hàng rỗng `[]` |
| 17 | Kiểm tra trạng thái đơn hàng ban đầu luôn là `pending` | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Thuộc tính `status` trong đơn hàng mới tạo phải bằng `"pending"` (FR-10) |
| 18 | Checkout kèm ghi chú đơn hàng (Order Notes) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "notes": "Giao giờ hành chính"}` | 200 OK | Lưu thông tin đơn hàng thành công kèm ghi chú giao hàng |

---

### Batch 2: Bảo mật Authentication/IDOR & Response Schema (17 test cases)

> **Phạm vi kiểm thử:**
> - **Bảo mật & Xác thực (SEC-02, SEC-03, IDOR):** Checkout không truyền Authorization header (401), Token sai/hết hạn (401), Bearer token rỗng (401), dùng token của User A để checkout (không thể checkout giỏ của User B - IDOR), SQLi payload trong địa chỉ, Reflected XSS trong địa chỉ, HTTP Method không hợp lệ.
> - **Response Schema & Boundary:** JSON Payload sai cú pháp (400), Payload chứa trường lạ/dư thừa (`role="admin"`), `total_amount` âm (400), `total_amount` dạng string (400), Schema validation (`id`, `status='pending'`, `total_amount > 0`), Content-Type `application/json`.

| STT | Test Case Name | Method | Endpoint | Request Header / Body | Expected Status | Expected Body / Response Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| 19 | Checkout khi chưa đăng nhập (Thiếu Authorization Header) | POST | `/api/checkout` | Header: *(Không gửi Authorization)*<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 401 Unauthorized | Thông báo yêu cầu đăng nhập để thanh toán (SEC-02) |
| 20 | Checkout với JWT Token không hợp lệ / Bị sửa đổi signature | POST | `/api/checkout` | Header: `Bearer invalid_jwt_token_123`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 401 Unauthorized | Từ chối truy cập do Token không hợp lệ |
| 21 | Checkout với JWT Token đã hết hạn (Expired Token) | POST | `/api/checkout` | Header: `Bearer <expiredToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 401 Unauthorized | Thông báo phiên đăng nhập đã hết hạn |
| 22 | Checkout với Authorization Header có Bearer rỗng | POST | `/api/checkout` | Header: `Bearer `<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 401 Unauthorized | Từ chối truy cập do thiếu Bearer token |
| 23 | Kiểm tra IDOR — Thanh toán không thể can thiệp vào giỏ hàng của User khác | POST | `/api/checkout` | Header: `Bearer <userA_Token>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK / 400 | Backend chỉ checkout sản phẩm trong giỏ của User A; KHÔNG tạo đơn từ giỏ của User B |
| 24 | Bảo mật SQL Injection trong trường `shipping_address` | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi' OR '1'='1"}` | 200 OK / 400 | Xử lý an toàn Parameterized Query; lưu chuỗi literal, KHÔNG bị lỗi SQL Syntax |
| 25 | Bảo mật Reflected XSS trong trường `shipping_address` | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "<script>alert('xss')</script>"}` | 200 OK | Địa chỉ được sanitize/escape an toàn, KHÔNG thi hành script khi render UI (SEC-04) |
| 26 | Gửi request Checkout với phương thức HTTP không hợp lệ (GET /api/checkout) | GET | `/api/checkout` | Header: `Bearer <userToken>` | 405 Method Not Allowed | Server từ chối phương thức GET cho endpoint checkout |
| 27 | JSON Payload bị lỗi cú pháp (Syntax Error / Invalid JSON) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"` *(thiếu dấu đóng `}`)* | 400 Bad Request | Thông báo lỗi cú pháp JSON payload |
| 28 | Payload chứa trường dư thừa cố ý leo thang quyền hạn (`"role": "admin"`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "role": "admin"}` | 200 OK / 400 | Server bỏ qua trường `role` dư thừa; tài khoản người dùng KHÔNG bị đổi thành admin |
| 29 | Payload có `total_amount` là số âm (`-200000`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": -200000, "shipping_address": "123 Le Loi"}` | 400 Bad Request / 200 OK | Backend từ chối giá trị âm hoặc tự động tính lại tổng tiền chính xác từ giỏ hàng |
| 30 | Payload có `total_amount` là dạng chuỗi ký tự (Non-numeric `"abc"`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": "abc", "shipping_address": "123 Le Loi"}` | 400 Bad Request / 200 OK | Thông báo lỗi kiểu dữ liệu hoặc tự tính lại tiền từ DB |
| 31 | Schema Validation — Kiểm tra sự tồn tại của thuộc tính `id` / `order_id` | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Response JSON chứa thuộc tính `id` (hoặc `order_id`) kiểu `Integer` dương |
| 32 | Schema Validation — Kiểm tra giá trị thuộc tính `status` | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Response JSON chứa `status === "pending"` (tuân thủ State Machine FR-10) |
| 33 | Schema Validation — Kiểm tra kiểu dữ liệu & giá trị `total_amount` trả về | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Response JSON chứa `typeof total_amount === 'number'` và `total_amount > 0` |
| 34 | Response Header Validation — Content-Type | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Response Header chứa `Content-Type: application/json` |
| 35 | Boundary — `total_amount` = 0 khi giỏ hàng có sản phẩm | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 0, "shipping_address": "123 Le Loi"}` *(Giỏ có hàng 200k)* | 200 OK | Backend bỏ qua `total_amount = 0` do Client truyền và tự tính lại đúng 200,000đ |

---

### Authoritative audit and final AI inventory

> **Fixture contract cho mọi dòng NEWMAN:** tạo user/session mới `u08-<case>-<runId>` và cart riêng; tính `serverTotal = Σ(current price × quantity)` từ fixture ngay trước checkout. Success oracle là 200 JSON, đúng một order mới `pending` có `total_amount = serverTotal`, rồi cart rỗng. Rejection oracle nêu status cụ thể, JSON error, không order mới và cart giữ nguyên. Không dùng fixed user/cart/order ID.

| ID | Verdict | Technical reason | Final correction | Execution class |
| --- | --- | --- | --- | --- |
| TC-FR08-AI-001 | VALID | Happy path đúng contract nhưng thiếu isolated fixture. | Fresh populated cart; body `total_amount=serverTotal`, unique valid address; áp dụng success oracle chung. | NEWMAN |
| TC-FR08-AI-002 | VALID | Empty-cart rejection có state oracle rõ. | Fresh user có cart rỗng; body xác định; 400 JSON, zero new order, cart vẫn rỗng. | NEWMAN |
| TC-FR08-AI-003 | INCOMPLETE | Contract không có stock field, stock mutation endpoint hay fixture tạo out-of-stock. | Giữ thiết kế stock race nhưng không chạy/không chọn 400 hay 409 khi SUT không có black-box stock hook. | EXCLUDED |
| TC-FR08-AI-004 | VALID | Empty required address có deterministic rejection. | Fresh populated cart; `shipping_address=""`; 400, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-005 | VALID | Whitespace-only phải không tạo địa chỉ giao hàng hữu dụng. | Fresh populated cart; address ba spaces; 400, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-006 | INCOMPLETE | “Thiếu chi tiết đường” không được contract định nghĩa và AI cho hai status. | Replacement: bỏ hẳn `shipping_address`; 400, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-007 | INVALID | `phone` không thuộc checkout body đã document. | Replacement: `shipping_address:null`; 400, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-008 | INCOMPLETE | Không có max length 500 trong contract. | Replacement type boundary: `shipping_address` là object; 400, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-009 | VALID | Server bắt buộc không tin client total. | Fresh cart có known `serverTotal`; gửi `total_amount=1`; 200, order total đúng `serverTotal`, cart rỗng. | NEWMAN |
| TC-FR08-AI-010 | INVALID | Coupon `SAVE10` là FR-09, không có trong selected contract. | Không sửa thành giả định coupon khác; giữ provenance và loại khỏi FR-08 execution. | EXCLUDED |
| TC-FR08-AI-011 | INVALID | `BIGBUY` và fixed discount không được document. | Loại khỏi selected FR-08 execution; không tuyên bố kết quả. | EXCLUDED |
| TC-FR08-AI-012 | INVALID | Coupon expiry/C2 không thuộc contract đã xác minh. | Loại khỏi selected FR-08 execution; cần FR-09 contract riêng. | EXCLUDED |
| TC-FR08-AI-013 | INVALID | Coupon minimum/C3 không thuộc contract đã xác minh. | Loại khỏi selected FR-08 execution; cần FR-09 fixture/rule riêng. | EXCLUDED |
| TC-FR08-AI-014 | INVALID | `max_uses_per_user`/C5 không thuộc contract. | Loại khỏi selected FR-08 execution; không fabricate coupon fixture. | EXCLUDED |
| TC-FR08-AI-015 | INVALID | `coupon_code` không nằm trong documented body. | Loại khỏi selected FR-08 execution; không đặt multi-status oracle cho hành vi ngoài contract. | EXCLUDED |
| TC-FR08-AI-016 | INCOMPLETE | Original đúng cart-clear rule nhưng thiếu isolated pre/postcondition. | Fresh populated cart; checkout 200; exactly one order với `serverTotal`; follow-up cart read là empty. | NEWMAN |
| TC-FR08-AI-017 | VALID | Initial `pending` là FR-10 invariant. | Fresh populated cart; 200; newly created order được xác định bằng run marker có status đúng `pending`, cart rỗng. | NEWMAN |
| TC-FR08-AI-018 | INVALID | `notes` không thuộc documented body/persistence contract. | Giữ provenance và loại khỏi execution tới khi có field contract. | EXCLUDED |
| TC-FR08-AI-019 | VALID | Missing auth phải bị chặn trước mutation. | Fresh populated cart; không Authorization; 401 JSON, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-020 | VALID | Invalid JWT có 401 oracle. | Fresh populated cart; malformed/signed-invalid token; 401, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-021 | INCOMPLETE | Expired JWT là auth boundary hữu ích nhưng SUT không cung cấp TTL/clock control, signing key hay token-expiry fixture xác định. | Giữ original expired-token intent nhưng loại khỏi execution; token chỉ sửa claim `exp` sẽ hỏng chữ ký và chỉ chứng minh invalid-signature, không chứng minh expiry. | EXCLUDED |
| TC-FR08-AI-022 | VALID | Empty bearer là credentials không hợp lệ. | Fresh populated cart; `Authorization: Bearer `; 401, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-023 | INCOMPLETE | Original thiếu hai user/cart fixtures nên chưa chứng minh ownership. | Fresh users A/B có totals khác nhau; token A checkout; 200 order chỉ chứa A cart/`serverTotalA`, A cart empty, B cart/order unchanged. | NEWMAN |
| TC-FR08-AI-024 | INCOMPLETE | Original cho 200/400 và không có persistence oracle. | Fresh cart; unique quote/SQL sentinel trong address; 200, exactly one order, literal address round-trips, total đúng server, không SQL error. | NEWMAN |
| TC-FR08-AI-025 | INCOMPLETE | API response không chứng minh HTML rendering an toàn. | Checkout fixture address chứa unique script sentinel, sau đó browser admin/order view phải render text, không script/event node; API setup không được tính là DOM proof. | BROWSER-MANUAL |
| TC-FR08-AI-026 | INVALID | GET không thuộc selected `POST /api/checkout` execution scope. | Giữ unsupported-method idea làm provenance nhưng không tạo NEWMAN assertion ngoài allowed method. | EXCLUDED |
| TC-FR08-AI-027 | VALID | Malformed JSON phải bị parser chặn. | Fresh populated cart; `Content-Type: application/json`, raw body thiếu closing brace; 400 JSON, zero order, cart unchanged. | NEWMAN |
| TC-FR08-AI-028 | INCOMPLETE | Unknown-field policy không được contract chốt; 200/400 là mơ hồ. | Không tự đặt ignore/reject policy cho `role`; loại khỏi execution, privilege escalation được kiểm contract-grounded ở FR-18. | EXCLUDED |
| TC-FR08-AI-029 | INCOMPLETE | Contract bắt buộc không tin client total nhưng không chốt reject hay ignore cho kiểu số âm. | Fresh cart và snapshot order count; gửi client total âm; status không phải 500 và body JSON. Nếu accepted: đúng một order `pending` có total bằng positive `serverTotal`, không lưu giá trị âm, cart empty. Nếu rejected: không order mới và cart/order snapshot unchanged. Mọi trạng thái khác fail. | NEWMAN |
| TC-FR08-AI-030 | INCOMPLETE | Contract bắt buộc server recalculation nhưng không chốt parser policy cho client total dạng string. | Fresh cart và snapshot order count; gửi client total `"abc"`; status không phải 500 và body JSON. Nếu accepted: đúng một order `pending` có total bằng positive `serverTotal`, không lưu `"abc"`, cart empty. Nếu rejected: không order mới và cart/order snapshot unchanged. Mọi trạng thái khác fail. | NEWMAN |
| TC-FR08-AI-031 | INCOMPLETE | `id` hoặc `order_id` là field-name oracle mơ hồ. | Fresh cart; 200 JSON; postcondition tìm đúng một new order bằng unique address/run marker và positive integer server-side ID, không phụ thuộc response alias. | NEWMAN |
| TC-FR08-AI-032 | VALID | `pending` là deterministic state oracle. | Fresh cart; 200; exactly one order, status `pending`, total server-calculated, cart empty. | NEWMAN |
| TC-FR08-AI-033 | VALID | Total response cần gắn exact cart fixture. | Fresh cart; 200; persisted `total_amount` là finite positive number bằng `serverTotal`, cart empty. | NEWMAN |
| TC-FR08-AI-034 | VALID | JSON media type là header assertion trực tiếp. | Fresh cart; success oracle chung và response `Content-Type` chứa `application/json`. | NEWMAN |
| TC-FR08-AI-035 | INCOMPLETE | Cart precondition chưa được cô lập nhưng recalculation rule rõ. | Fresh non-empty cart; client total 0; 200, exactly one order total bằng nonzero `serverTotal`, cart empty. | NEWMAN |

## 2. Authoritative human-designed inventory (10 cases)

> Barrier notation: `READY-A/B` means both sessions have completed setup; `RELEASE-X` permits the named mutation; checkout starts only after the stated barrier. Each runnable case uses a fresh user/cart and verifies order count, final cart, and exact server-calculated total. Stock rows are excluded because the public SUT exposes neither stock state nor a stock mutation hook.

| ID | Final corrected scenario and deterministic oracle | Execution class | Why AI missed it |
| --- | --- | --- | --- |
| TC-FR08-HUMAN-001 | Browser sessions A/B share one fresh user. At `READY-A/B`, B empties cart and confirms empty, then `RELEASE-A`; A clicks checkout. UI/API shows 400, zero order, cart remains empty. | BROWSER-MANUAL | Requires observable multi-tab ordering. |
| TC-FR08-HUMAN-002 | Original requires stock=1 then another user consumes it. No documented stock field/mutation endpoint can establish or observe the barrier; no 400/409 is claimed. | EXCLUDED | Requires unavailable inventory control. |
| TC-FR08-HUMAN-003 | Browser double-click after `READY-A`; capture both network requests. Exactly one is 200 and one is 400 cart-empty, exactly one order has `serverTotal`, final cart empty. | BROWSER-MANUAL | UI event and concurrent network observation. |
| TC-FR08-HUMAN-004 | Coupon-array attack belongs to FR-09 and `coupon_code` is absent from the verified checkout body; no execution result is claimed. | EXCLUDED | Cross-feature schema assumption. |
| TC-FR08-HUMAN-005 | Session A records old client total; session B changes cart quantity and confirms new `serverTotal`, then `RELEASE-A`. A submits stale total; 200 order uses new server total, exactly one order, cart empty. | NEWMAN | Requires state change between read and write. |
| TC-FR08-HUMAN-006 | API sessions A/B: after `READY-A/B`, B deletes every cart item and verifies empty, then releases A checkout; 400, zero order, empty cart. | NEWMAN | Explicit callback barrier is uncommon in generated cases. |
| TC-FR08-HUMAN-007 | Last-stock race remains valuable but no black-box stock hook/field exists; retain design without selecting 400 or 409 and without run claim. | EXCLUDED | Requires atomic inventory fixture. |
| TC-FR08-HUMAN-008 | Two POSTs for one fresh cart are released together after `READY-A/B`; at most one 200, exactly one persisted order with `serverTotal`, final cart empty, no duplicate amount/order marker. | NEWMAN | Same-mutation concurrency needs synchronization. |
| TC-FR08-HUMAN-009 | Session B removes the last cart item and verifies empty before releasing A POST; 400, zero order, cart empty. | NEWMAN | Tests commit-time state rather than stale UI state. |
| TC-FR08-HUMAN-010 | EXCLUDED duplicate of authoritative HUMAN-005: cùng cart quantity change trước checkout, cùng stale client total và cùng exact server-total/cart oracle; giữ ID làm provenance nhưng không đếm như NEWMAN scenario độc lập. | EXCLUDED | Original wording added address/coupon context without a distinct documented requirement or observable oracle. |
