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

### Bảng Kiểm Toán Audit (35 Test Cases AI Sinh - FR-08)

| STT | Test Case ID | Trạng thái Audit | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- |
| 1 | TC-FR08-AI-001 | [Manual by user] | [Manual by user] |
| 2 | TC-FR08-AI-002 | [Manual by user] | [Manual by user] |
| 3 | TC-FR08-AI-003 | [Manual by user] | [Manual by user] |
| 4 | TC-FR08-AI-004 | [Manual by user] | [Manual by user] |
| 5 | TC-FR08-AI-005 | [Manual by user] | [Manual by user] |
| 6 | TC-FR08-AI-006 | [Manual by user] | [Manual by user] |
| 7 | TC-FR08-AI-007 | [Manual by user] | [Manual by user] |
| 8 | TC-FR08-AI-008 | [Manual by user] | [Manual by user] |
| 9 | TC-FR08-AI-009 | [Manual by user] | [Manual by user] |
| 10 | TC-FR08-AI-010 | [Manual by user] | [Manual by user] |
| 11 | TC-FR08-AI-011 | [Manual by user] | [Manual by user] |
| 12 | TC-FR08-AI-012 | [Manual by user] | [Manual by user] |
| 13 | TC-FR08-AI-013 | [Manual by user] | [Manual by user] |
| 14 | TC-FR08-AI-014 | [Manual by user] | [Manual by user] |
| 15 | TC-FR08-AI-015 | [Manual by user] | [Manual by user] |
| 16 | TC-FR08-AI-016 | [Manual by user] | [Manual by user] |
| 17 | TC-FR08-AI-017 | [Manual by user] | [Manual by user] |
| 18 | TC-FR08-AI-018 | [Manual by user] | [Manual by user] |
| 19 | TC-FR08-AI-019 | [Manual by user] | [Manual by user] |
| 20 | TC-FR08-AI-020 | [Manual by user] | [Manual by user] |
| 21 | TC-FR08-AI-021 | [Manual by user] | [Manual by user] |
| 22 | TC-FR08-AI-022 | [Manual by user] | [Manual by user] |
| 23 | TC-FR08-AI-023 | [Manual by user] | [Manual by user] |
| 24 | TC-FR08-AI-024 | [Manual by user] | [Manual by user] |
| 25 | TC-FR08-AI-025 | [Manual by user] | [Manual by user] |
| 26 | TC-FR08-AI-026 | [Manual by user] | [Manual by user] |
| 27 | TC-FR08-AI-027 | [Manual by user] | [Manual by user] |
| 28 | TC-FR08-AI-028 | [Manual by user] | [Manual by user] |
| 29 | TC-FR08-AI-029 | [Manual by user] | [Manual by user] |
| 30 | TC-FR08-AI-030 | [Manual by user] | [Manual by user] |
| 31 | TC-FR08-AI-031 | [Manual by user] | [Manual by user] |
| 32 | TC-FR08-AI-032 | [Manual by user] | [Manual by user] |
| 33 | TC-FR08-AI-033 | [Manual by user] | [Manual by user] |
| 34 | TC-FR08-AI-034 | [Manual by user] | [Manual by user] |
| 35 | TC-FR08-AI-035 | [Manual by user] | [Manual by user] |

---

### Audit kết luận chi tiết

> **VALID**: oracle phù hợp contract; **INCOMPLETE**: hướng kiểm thử đúng nhưng còn thiếu fixture/oracle/điều kiện; **INVALID**: kỳ vọng trái đặc tả hoặc kiểm sai phạm vi API.

| STT | Nhãn | Lý do kỹ thuật |
|---:|---|---|
| 1 | VALID | Happy path có auth, body và trạng thái pending; cần fixture cart trị giá 200k. |
| 2 | VALID | Cart rỗng phải không tạo order; 400 là oracle hợp lý. |
| 3 | INCOMPLETE | Body không mô tả sản phẩm/số lượng vượt kho; cần fixture và chốt 400 hay 409. |
| 4 | VALID | Required shipping address rỗng phải bị từ chối. |
| 5 | VALID | Whitespace-only phải được trim/validate và trả lỗi. |
| 6 | INCOMPLETE | Đặc tả chỉ nhận chuỗi address; “đủ chi tiết” và 200/400 chưa có contract rõ. |
| 7 | INVALID | `phone` không thuộc schema body đã nêu; không thể yêu cầu validation riêng nếu đặc tả không hỗ trợ field này. |
| 8 | INCOMPLETE | Có thể là giới hạn hợp lệ nhưng thiếu max length chính thức và response oracle. |
| 9 | VALID | Không tin total từ client; phải tính từ cart/DB và so sánh chính xác. |
| 10 | INVALID | `SAVE10`, min value và coupon schema không được chứng minh trong FR-08; test phụ thuộc fixture/đặc tả ngoài. |
| 11 | INVALID | Tương tự TC10; mã `BIGBUY` và mức giảm không thuộc contract đã cung cấp. |
| 12 | INVALID | `EXPIRED` và C2 không có trong FR-08 contract; đây là giả định dữ liệu. |
| 13 | INVALID | Min-order coupon rule không được đặc tả; expected 400 không có cơ sở. |
| 14 | INVALID | max_uses_per_user/C5 không được nêu trong API contract. |
| 15 | INVALID | Coupon code không thuộc body chuẩn đã nêu; cần tài liệu coupon riêng trước khi test. |
| 16 | INCOMPLETE | Có thể là invariant nghiệp vụ nhưng cần xác nhận GET cart và atomic transaction trong đặc tả. |
| 17 | VALID | Order mới phải bắt đầu `pending` theo FR-10; cần kiểm cả DB side effect. |
| 18 | INCOMPLETE | “Ghi chú đơn hàng” chưa có field/contract; cần nêu body và expected persistence. |
| 19 | VALID | Thiếu Authorization phải trả 401 và không tạo order. |
| 20 | VALID | Token sai/hết hạn/bearer rỗng là boundary auth; cần tách case để oracle rõ. |
| 21 | INCOMPLETE | IDOR chưa có hai user/cart fixture và tiêu chí không tạo order; cần bổ sung. |
| 22 | INVALID | SQLi trong `shipping_address` không chứng minh field được dùng SQL; nên test input handling riêng với contract rõ. |
| 23 | INCOMPLETE | XSS chỉ có ý nghĩa khi address được render; API JSON không tự thực thi HTML, cần kiểm consumer UI. |
| 24 | VALID | Unsupported method phải không tạo side effect; 405 cần phù hợp routing contract. |
| 25 | INCOMPLETE | Thiếu Content-Type chưa nêu expected parser behavior; cần chốt 400/415 và header request. |
| 26 | VALID | GET tới POST-only endpoint là method contract kiểm được. |
| 27 | VALID | JSON syntax lỗi phải bị parser từ chối trước nghiệp vụ, thường 400. |
| 28 | VALID | Mass-assignment field phải bị bỏ qua hoặc từ chối; không đổi quyền. |
| 29 | INCOMPLETE | Nếu server tính lại total thì 200 có thể đúng, nhưng cần chốt validation và kiểm side effect. |
| 30 | INCOMPLETE | Tương tự TC29; cần phân biệt reject type với ignore client total. |
| 31 | VALID | Response phải có ID order dương và kiểu integer theo schema. |
| 32 | VALID | `pending` là invariant trạng thái khởi tạo. |
| 33 | VALID | Kiểu/giá trị total response phải phản ánh total đã tính; cần fixture cart. |
| 34 | VALID | Content-Type `application/json` là header assertion rõ. |
| 35 | INCOMPLETE | Cho phép 200 vì server bỏ qua total là hợp lý, nhưng phải xác nhận cart có hàng và không tạo duplicate. |

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR08-HUMAN-001 | Race condition — Checkout khi giỏ hàng vừa bị xóa/thay đổi ở tab khác | Concurrent State | 1. Mở 2 tab trình duyệt cùng giỏ hàng<br>2. Tab 2 xóa sạch giỏ hàng<br>3. Tab 1 bấm Checkout | Trả về 400 Bad Request ("Giỏ hàng rỗng"), không tạo đơn hàng rỗng | AI thiếu khả năng mô phỏng hành vi đa tab/đa phiên của người dùng thực tế |
| TC-FR08-HUMAN-002 | Race condition — Tồn kho bị giảm về 0 ngay trước thời điểm nhấn checkout | Concurrent Inventory | 1. User A chuẩn bị checkout sản phẩm X (còn 1 item trong kho)<br>2. User B checkout sản phẩm X thành công trước 1 giây<br>3. User A gửi request checkout | User A nhận lỗi 400/409 Conflict ("Sản phẩm hết hàng"), transaction rollback an toàn | AI không tự tạo được ngữ cảnh tranh chấp tài nguyên (Concurrency Race Condition) giữa 2 user |
| TC-FR08-HUMAN-003 | Double-click / Concurrent submission (Idempotency) | Idempotency | Gửi 2 request `POST /api/checkout` đồng thời trong khoảng thời gian < 50ms với cùng token | Chỉ có đúng 1 đơn hàng được tạo (200 OK), request thứ 2 bị chặn hoặc báo 400 (do giỏ đã bị xóa sau request 1) | AI chỉ sinh các request độc lập đơn lẻ, không kiểm thử tần suất gửi trùng lặp tức thời |
| TC-FR08-HUMAN-004 | Coupon stack attack — Cố gắng truyền mảng mã coupon | Security / Validation | Body: `{"shipping_address": "123 Le Loi", "coupon_code": ["SAVE10", "BIGBUY"]}` | Backend chỉ nhận 1 string coupon duy nhất hoặc từ chối 400 Bad Request, không cộng dồn mã | AI bỏ sót kiểm thử kiểu dữ liệu mảng (Array injection) trên trường coupon |
| TC-FR08-HUMAN-005 | Sửa đổi giá sản phẩm giữa lúc thêm vào giỏ và lúc checkout | Stale Price / Integrity | 1. User thêm SP A (giá 100k) vào giỏ<br>2. Admin sửa giá SP A lên 200k trong CSDL<br>3. User thực hiện Checkout | Total amount đơn hàng được tính theo giá hiện tại trong DB (200k), không bị dùng giá cũ stale price | AI không tự xây dựng kịch bản kiểm thử tích hợp (Integration) liên vết giữa Admin CRUD và User Checkout |

### Bổ sung human-designed về race condition và trạng thái đa phiên

| ID | Kịch bản và cách thực hiện | Expected result | Vì sao AI thường bỏ sót |
|---|---|---|---|
| TC-FR08-HUMAN-006 | Tab A đọc cart có hàng; tab B xóa cart; ngay sau đó tab A POST checkout | 400, không tạo order, không trừ kho; transaction thấy state mới nhất | AI thường mô hình hóa request độc lập, không có timeline giữa các tab. |
| TC-FR08-HUMAN-007 | User A giữ cart có 1 sản phẩm; User B mua item cuối cùng trước khi A checkout | A nhận 400/409; không tạo order một phần và không âm kho | AI bỏ qua tranh chấp tài nguyên liên user và atomic stock check. |
| TC-FR08-HUMAN-008 | Hai POST checkout cùng user/token trong <50ms | Tối đa một order thành công; request còn lại lỗi idempotency/cart-empty; không double charge | AI thiên về happy path và không sinh cùng một mutation đồng thời. |
| TC-FR08-HUMAN-009 | Tab A chuẩn bị checkout; tab B đổi quantity từ 1 xuống 0 rồi A gửi request | Server dùng cart tại commit time, trả lỗi rỗng/invalid; không dùng snapshot cũ | AI hiếm khi kiểm state thay đổi giữa đọc và ghi. |
| TC-FR08-HUMAN-010 | Tab A checkout; tab B đổi coupon/địa chỉ trong lúc transaction A đang xử lý | Order dùng một snapshot nhất quán; không trộn giá/coupon/address giữa hai phiên | AI thường không kiểm consistency giữa nhiều field cập nhật cạnh tranh. |
