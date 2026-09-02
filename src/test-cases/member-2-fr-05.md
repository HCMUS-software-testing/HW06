# Test Cases & Audit - FR-05: Liệt kê và tìm kiếm sản phẩm

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoints:**
- `GET /api/products` — Lấy danh sách sản phẩm (api_specification.md §3.1)
- `GET /api/products?search=keyword` — Tìm kiếm sản phẩm theo tên (api_specification.md §3.1)

> **Phạm vi cuối cùng:** chỉ FR-05 `GET /api/products[?search=...]`. Nội dung AI gốc ở các dòng 10–15 và 32 bên dưới vẫn được giữ nguyên làm provenance lịch sử FR-06; phần sửa cuối trong bảng audit mới là intent có hiệu lực và không tự động hóa `GET /api/products/:id` dưới FR-05.

**Kỹ thuật:** Phân hoạch miền (Domain Partitioning), Kiểm thử Bảo mật (SEC-01..SEC-07), Kiểm tra Response Schema  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` §3.1–§3.2 & `eshop-sut/README.md` FR-05, FR-06, SEC-04, SEC-05

---

## 1. Danh Sách Test Cases AI Sinh (35 Test Cases) & Kiểm Toán Audit

### Batch 1: Phân hoạch miền (Domain Partitioning) — 15 test cases

> **Phân vùng miền áp dụng:**
> - **GET /api/products**: Không tham số (danh sách đầy đủ)
> - **GET /api/products?search=keyword**: Từ khóa hợp lệ, từ khóa không tồn tại, từ khóa rỗng, ký tự đặc biệt, ký tự Unicode/tiếng Việt, từ khóa rất dài
> - **GET /api/products/:id**: ID tồn tại, ID = 0, ID âm, ID chuỗi ký tự, ID rất lớn, ID thập phân

| STT | Test Case Name | Method | Endpoint | Query/Path Params | Expected Status | Expected Schema/Body |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Lấy danh sách tất cả sản phẩm (không tham số) | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON các sản phẩm, mỗi phần tử chứa: `id` (integer), `name` (string), `price` (number > 0), `description` (string), `imageUrl` (string), `category_id` (integer) |
| 2 | Tìm kiếm với từ khóa hợp lệ tồn tại trong DB | GET | `/api/products` | `?search=phone` | 200 OK | Mảng JSON chứa ≥ 1 sản phẩm có `name` chứa "phone" (case-insensitive) |
| 3 | Tìm kiếm với từ khóa hợp lệ KHÔNG tồn tại trong DB | GET | `/api/products` | `?search=xyznonexistent999` | 200 OK | Mảng JSON rỗng `[]` (empty state — README FR-05: "Khi không có kết quả tìm kiếm phải hiển thị thông báo empty state phù hợp") |
| 4 | Tìm kiếm với chuỗi rỗng (empty string) | GET | `/api/products` | `?search=` | 200 OK | Mảng JSON trả về toàn bộ sản phẩm (tương đương không lọc) hoặc mảng rỗng tùy implementation |
| 5 | Tìm kiếm với ký tự đặc biệt ASCII | GET | `/api/products` | `?search=!@#$%^&*()` | 200 OK | Mảng JSON rỗng `[]` hoặc sản phẩm phù hợp nếu có; server KHÔNG crash, KHÔNG trả 500 |
| 6 | Tìm kiếm với ký tự Unicode / tiếng Việt có dấu | GET | `/api/products` | `?search=điện thoại` | 200 OK | Mảng JSON rỗng hoặc sản phẩm có tên chứa "điện thoại"; chứng minh hỗ trợ UTF-8 |
| 7 | Tìm kiếm với từ khóa rất dài (> 255 ký tự) | GET | `/api/products` | `?search=aaaa...` (256+ chars) | 200 OK hoặc 400 Bad Request | Server xử lý gọn gàng: trả mảng rỗng hoặc lỗi validation, KHÔNG crash 500 |
| 8 | Tìm kiếm với khoảng trắng (spaces only) | GET | `/api/products` | `?search=%20%20%20` | 200 OK | Mảng JSON: toàn bộ sản phẩm (nếu trim) hoặc mảng rỗng (nếu exact match) |
| 9 | Tìm kiếm với từ khóa chỉ chứa chữ số | GET | `/api/products` | `?search=12345` | 200 OK | Mảng JSON rỗng hoặc sản phẩm có tên chứa "12345" |
| 10 | Lấy chi tiết sản phẩm với ID tồn tại (valid integer) | GET | `/api/products/:id` | `:id = 1` | 200 OK | Object JSON chứa đầy đủ: `id` (= 1), `name`, `price`, `description`, `imageUrl`, `category_id` |
| 11 | Lấy chi tiết sản phẩm với ID = 0 (boundary) | GET | `/api/products/:id` | `:id = 0` | 404 Not Found | Thông báo lỗi product không tồn tại |
| 12 | Lấy chi tiết sản phẩm với ID âm | GET | `/api/products/:id` | `:id = -1` | 404 Not Found hoặc 400 Bad Request | Thông báo lỗi: ID không hợp lệ hoặc product không tồn tại |
| 13 | Lấy chi tiết sản phẩm với ID là chuỗi ký tự (non-numeric) | GET | `/api/products/:id` | `:id = abc` | 400 Bad Request hoặc 404 | Server xử lý gọn gàng: thông báo lỗi parameter không hợp lệ, KHÔNG crash 500 |
| 14 | Lấy chi tiết sản phẩm với ID rất lớn (không tồn tại) | GET | `/api/products/:id` | `:id = 999999999` | 404 Not Found | Thông báo lỗi product không tồn tại |
| 15 | Lấy chi tiết sản phẩm với ID là số thập phân (float) | GET | `/api/products/:id` | `:id = 1.5` | 400 Bad Request hoặc 404 | Server xử lý gọn gàng: ID phải là integer, không chấp nhận float |

---

### Batch 2: Bảo mật (SQLi/XSS) & Response Schema Validation — 20 test cases

> **Phạm vi kiểm thử:**
> - **Bảo mật (SEC-01..SEC-07):** SQL Injection (`' OR '1'='1`, `UNION SELECT`), Reflected XSS (`<script>`, `onerror`), Parameter Pollution/Length, Null byte injection, Emojis/Unicode.
> - **Response Schema & Types:** Kiểm tra cấu trúc mảng/đối tượng JSON, kiểu dữ liệu `id` (integer), `price` (number > 0), `name`/`description`/`imageUrl` (string), `category_id` (integer), `Content-Type: application/json`.

| STT | Test Case Name | Method | Endpoint | Query/Path Params | Expected Status | Expected Schema/Body |
| --- | --- | --- | --- | --- | --- | --- |
| 16 | SQL Injection — Tautology Payload | GET | `/api/products` | `?search=' OR '1'='1` | 200 OK | Mảng rỗng `[]` hoặc tìm đúng chuỗi literal; KHÔNG rò rỉ toàn bộ DB (SEC-05 Parameterized Query) |
| 17 | SQL Injection — Union Based Payload | GET | `/api/products` | `?search=' UNION SELECT 1,2,3,4,5,6--` | 200 OK / 400 Bad Request | Mảng rỗng `[]` hoặc lỗi validation; KHÔNG rò rỉ bảng dữ liệu khác |
| 18 | SQL Injection — Time Delay / Stacked Queries | GET | `/api/products` | `?search='; SELECT pg_sleep(5)--` | 200 OK / 400 Bad Request | Server phản hồi lập tức (< 1s), KHÔNG bị kẹt delay |
| 19 | SQL Injection — Comment Out Syntax | GET | `/api/products` | `?search=phone'--` | 200 OK | Mảng rỗng `[]` hoặc kết quả tìm kiếm an toàn; KHÔNG bị 500 SQL syntax error |
| 20 | Reflected XSS — Script Tag Injection | GET | `/api/products` | `?search=<script>alert('XSS')</script>` | 200 OK | Mảng rỗng `[]`; từ khóa được escape an toàn, KHÔNG thi hành HTML/JS (SEC-04) |
| 21 | Reflected XSS — Event Handler Payload | GET | `/api/products` | `?search=<img src=x onerror=alert(1)>` | 200 OK | Mảng rỗng `[]`; dữ liệu phản hồi được sanitize an toàn |
| 22 | Reflected XSS — JavaScript Pseudo-protocol | GET | `/api/products` | `?search=javascript:alert(1)` | 200 OK | Tra cứu như chuỗi thường, trả về `[]`, an toàn |
| 23 | Oversized Parameter — Buffer Overflow Attempt | GET | `/api/products` | `?search=` + 5000 chars `'A'` | 400 Bad Request / 200 OK | Mảng rỗng `[]` hoặc 400 Bad Request; Server KHÔNG crash 500 |
| 24 | Null Byte Injection | GET | `/api/products` | `?search=phone%00.php` | 200 OK / 400 Bad Request | Xử lý an toàn chuỗi kết thúc null byte, KHÔNG lộ file hệ thống |
| 25 | Multi-byte Unicode Emojis Parameter | GET | `/api/products` | `?search=📱💻🔥` | 200 OK | Mảng JSON trả về rỗng `[]`, không bị lỗi mã hóa UTF-8 |
| 26 | Schema Validation — Kiểu dữ liệu thuộc tính `id` | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON sản phẩm: `typeof id === 'number'` và `Number.isInteger(id) === true` |
| 27 | Schema Validation — Kiểu dữ liệu thuộc tính `name` | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON sản phẩm: `typeof name === 'string'` và `name.length > 0` |
| 28 | Schema Validation — Kiểu dữ liệu & Giá trị thuộc tính `price` | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON sản phẩm: `typeof price === 'number'` và `price > 0` |
| 29 | Schema Validation — Kiểu dữ liệu thuộc tính `description` | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON sản phẩm: `typeof description === 'string'` |
| 30 | Schema Validation — Kiểu dữ liệu thuộc tính `imageUrl` | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON sản phẩm: `typeof imageUrl === 'string'` |
| 31 | Schema Validation — Kiểu dữ liệu thuộc tính `category_id` | GET | `/api/products` | *(không có)* | 200 OK | Mảng JSON sản phẩm: `typeof category_id === 'number'` và `Number.isInteger(category_id)` |
| 32 | Schema Validation — Cấu trúc đối tượng chi tiết sản phẩm | GET | `/api/products/1` | `:id = 1` | 200 OK | JSON Object chứa chính xác 6 thuộc tính: `id`, `name`, `price`, `description`, `imageUrl`, `category_id` |
| 33 | Response Header Validation — Content-Type | GET | `/api/products` | *(không có)* | 200 OK | Response header `Content-Type` chứa `application/json` |
| 34 | Schema Validation — Cấu trúc danh sách rỗng (Empty State) | GET | `/api/products` | `?search=nonexistent_xyz` | 200 OK | Trả về JSON Array `[]` với `Array.isArray(body) === true` và `body.length === 0` |
| 35 | Schema Validation — Không rò rỉ trường dữ liệu nhạy cảm | GET | `/api/products` | *(không có)* | 200 OK | Mảng sản phẩm KHÔNG chứa các thuộc tính ẩn/nhạy cảm như `password`, `secret`, `internal_id` |

---

### Authoritative audit and final AI inventory

> `Verdict` đánh giá **nội dung AI gốc**; `Final correction` là oracle có hiệu lực cho Task 3. Trường hợp contract không quy định chuẩn hóa/giới hạn cụ thể dùng invariant duy nhất: không 500, body là JSON array và GET không làm đổi dữ liệu. SEC-04 ở lớp DOM không được suy ra từ JSON.

| ID | Verdict | Technical reason | Final correction | Execution class |
| --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | VALID | Đúng endpoint list và có schema quan sát được. | Gọi không query; yêu cầu 200, `application/json`, body là array; mọi phần tử có `id`, `name`, `price`, `description`, `imageUrl`, `category_id`. | NEWMAN |
| TC-FR05-AI-002 | INCOMPLETE | Từ khóa `phone` không được gắn với fixture nên `≥1` không ổn định. | Lấy một `name` từ baseline làm keyword; 200 và mọi kết quả có tên chứa keyword đã chọn, đồng thời chứa ít nhất fixture nguồn. | NEWMAN |
| TC-FR05-AI-003 | VALID | Search tên không tồn tại có empty-array oracle rõ. | Dùng sentinel duy nhất theo run; 200, JSON array và length bằng 0; kiểm empty-state UI tách riêng. | NEWMAN |
| TC-FR05-AI-004 | INCOMPLETE | AI cho phép hai kết quả trái nhau cho `search=`. | So sánh `search=` với request không query; cả hai 200 và có cùng dãy product ID. | NEWMAN |
| TC-FR05-AI-005 | INCOMPLETE | “Sản phẩm phù hợp nếu có” không xác định fixture. | Dùng sentinel ASCII đặc biệt không có trong baseline; status không phải 500, body JSON array, không rò SQL/HTML error và dữ liệu baseline không đổi. | NEWMAN |
| TC-FR05-AI-006 | INCOMPLETE | Không có fixture tên tiếng Việt hay quy tắc accent-folding. | Search sentinel Unicode duy nhất không có trong baseline; 200, JSON array rỗng và UTF-8 hợp lệ. | NEWMAN |
| TC-FR05-AI-007 | INCOMPLETE | Contract không nêu max length và AI cho 200/400. | Gửi 256 ký tự; chỉ assert invariant contract-safe: status không phải 500, body JSON, GET không đổi baseline; ghi status quan sát riêng khi chạy. | NEWMAN |
| TC-FR05-AI-008 | INCOMPLETE | Contract không chốt trim spaces. | Gửi spaces-only; status không phải 500, body JSON array, không error leakage và baseline không đổi. | NEWMAN |
| TC-FR05-AI-009 | INCOMPLETE | Thiếu fixture tên số và điều kiện match. | Dùng sentinel chữ số không có trong baseline; 200, array rỗng và không 500. | NEWMAN |
| TC-FR05-AI-010 | INVALID | Original dùng product-detail FR-06 ngoài FR-05. | Replacement FR-05: `search=` và query bị bỏ trống phải trả cùng dãy ID, 200 JSON array. | NEWMAN |
| TC-FR05-AI-011 | INVALID | Original dùng product-detail FR-06 ngoài FR-05. | Replacement FR-05: gửi hai `search` values; status không phải 500, body JSON array, không error leakage và GET không đổi baseline. | NEWMAN |
| TC-FR05-AI-012 | INVALID | Original dùng product-detail FR-06 ngoài FR-05 và có multi-status oracle. | Replacement FR-05: `search=%70hone` và `search=phone` phải trả cùng status 200 và cùng dãy ID sau percent-decoding. | NEWMAN |
| TC-FR05-AI-013 | INVALID | Original dùng product-detail FR-06 ngoài FR-05 và có multi-status oracle. | Replacement FR-05: hai sentinel SQLi boolean true/false phải cùng 200, cùng array, không mở rộng tới baseline và không lộ lỗi DB. | NEWMAN |
| TC-FR05-AI-014 | INVALID | Original là product detail FR-06. | Replacement FR-05: search response phải 200 và `Content-Type` chứa `application/json`. | NEWMAN |
| TC-FR05-AI-015 | INVALID | Original là product detail FR-06 và có multi-status oracle. | Replacement FR-05: unique raw HTML sentinel không xuất hiện trong serialized product JSON; 200 array và cardinality không vượt baseline. | NEWMAN |
| TC-FR05-AI-016 | VALID | Tautology payload là black-box SEC-05 probe phù hợp. | So với baseline và sentinel literal; 200 array, không mở rộng tới toàn bộ baseline, không có SQL error token. | NEWMAN |
| TC-FR05-AI-017 | INCOMPLETE | Original cho phép 200/400 và không chốt body. | Chốt 200 JSON array; union payload không làm cardinality vượt baseline và body không lộ schema/SQL error. | NEWMAN |
| TC-FR05-AI-018 | INCOMPLETE | `pg_sleep` phụ thuộc DB và ngưỡng 1 giây phụ thuộc môi trường. | Giữ như thiết kế nghiên cứu timing, không có oracle black-box ổn định khi contract không xác nhận PostgreSQL hay latency budget. | EXCLUDED |
| TC-FR05-AI-019 | VALID | Comment syntax có thể kiểm bằng cardinality và error leakage. | 200 JSON array, không nhiều hơn baseline, không chứa SQL syntax/stack trace. | NEWMAN |
| TC-FR05-AI-020 | INCOMPLETE | JSON không chứng minh script có thực thi trong DOM. | Phần API duy nhất: 200 array, unique script sentinel không bị phản chiếu và không mở rộng kết quả; DOM được tách sang manual rows. | NEWMAN |
| TC-FR05-AI-021 | INCOMPLETE | Escape/sanitize là thuộc tính của consumer HTML, không phải array JSON. | Mở trang search với event-handler sentinel; payload chỉ là text, không tạo element/event handler, chỉ một `h1`, empty state xuất hiện. | BROWSER-MANUAL |
| TC-FR05-AI-022 | INCOMPLETE | `javascript:` chỉ nguy hiểm tại DOM/URL sink. | Mở browser với unique `javascript:` keyword; loading xuất hiện trước response, sau đó empty state, một `h1`, không navigation/script execution. | BROWSER-MANUAL |
| TC-FR05-AI-023 | INCOMPLETE | Contract không nêu giới hạn 5000 ký tự và AI cho hai status. | Status không phải 500, body JSON, không error leakage và GET không đổi baseline; status thực tế ghi sau execution. | NEWMAN |
| TC-FR05-AI-024 | INCOMPLETE | “Không lộ file” lệch data flow của search. | Percent-decode null byte safely: status không phải 500, body JSON array, không stack trace/path leakage và baseline không đổi. | NEWMAN |
| TC-FR05-AI-025 | VALID | UTF-8 JSON là oracle trực tiếp. | Unique emoji sentinel: 200, valid UTF-8 JSON array, length 0. | NEWMAN |
| TC-FR05-AI-026 | VALID | Integer ID là schema assertion ổn định. | Baseline 200; từng `id` là positive integer. | NEWMAN |
| TC-FR05-AI-027 | VALID | Non-empty product name là schema invariant. | Baseline 200; từng `name` là non-empty string. | NEWMAN |
| TC-FR05-AI-028 | VALID | Positive numeric price là schema invariant. | Baseline 200; từng `price` là finite number lớn hơn 0. | NEWMAN |
| TC-FR05-AI-029 | VALID | Description type có thể kiểm trực tiếp. | Baseline 200; từng `description` là string. | NEWMAN |
| TC-FR05-AI-030 | VALID | `imageUrl` string có thể kiểm trực tiếp; format URL không được contract yêu cầu. | Baseline 200; từng `imageUrl` là string, không thêm URL-format oracle. | NEWMAN |
| TC-FR05-AI-031 | VALID | `category_id` integer là schema assertion. | Baseline 200; từng `category_id` là integer. | NEWMAN |
| TC-FR05-AI-032 | INVALID | Original kiểm object detail FR-06 và “exactly six fields” quá cứng. | Replacement FR-05: list là array; mỗi item chứa ít nhất sáu required fields, cho phép metadata bổ sung. | NEWMAN |
| TC-FR05-AI-033 | VALID | Content-Type là response contract trực tiếp. | Baseline 200 và media type chuẩn hóa bằng `application/json`. | NEWMAN |
| TC-FR05-AI-034 | VALID | Sentinel không tồn tại tạo empty-array oracle xác định. | Unique no-match sentinel trả 200 và đúng `[]`. | NEWMAN |
| TC-FR05-AI-035 | INCOMPLETE | Denylist gốc chưa gắn data contract và chưa nói nested fields. | Recursively kiểm response không có key case-insensitive `password`, `secret`, `token`, `internal_id`; 200 JSON array. | NEWMAN |

## 2. Authoritative human-designed inventory (10 cases)

> Với case kết hợp API/UI, cột oracle ghi rõ nửa API được NEWMAN nào đảm nhiệm; ID của dòng này chỉ đại diện một execution class.

| ID | Final corrected scenario and deterministic oracle | Execution class | Why AI missed it |
| --- | --- | --- | --- |
| TC-FR05-HUMAN-001 | Gửi hai sentinel blind-SQLi chỉ khác `1=1`/`1=2`; cả hai 200, cùng JSON array, không lớn hơn baseline, không SQL error. | NEWMAN | Cần so sánh vi sai nhiều response. |
| TC-FR05-HUMAN-002 | Browser search unique SVG sentinel: hiển thị nguyên văn như text, không có `svg`/event node, đúng một `h1`, loading rồi empty state. Nửa API non-reflection do AI-015 kiểm. | BROWSER-MANUAL | AI thường dừng ở JSON và không kiểm DOM sink. |
| TC-FR05-HUMAN-003 | Duplicate `search=known&search=other`: status không phải 500, body JSON array, không error leakage và GET không đổi baseline. | NEWMAN | HTTP parameter pollution thường bị bỏ sót. |
| TC-FR05-HUMAN-004 | Original gọi product-detail/path traversal FR-06; giữ làm provenance nhưng không thuộc endpoint FR-05 được chọn. | EXCLUDED | AI mở rộng nhầm sang path endpoint lân cận. |
| TC-FR05-HUMAN-005 | Original so sánh list với product detail FR-06; không được tính hay chạy dưới FR-05. | EXCLUDED | AI gộp hai FR thành một data-flow case. |
| TC-FR05-HUMAN-006 | Browser lần lượt search empty và SQLi sentinel; keyword chỉ là text, một `h1`, loading/empty state đúng, không script. Nửa API empty normalization do AI-010 và SQLi cardinality do AI-016 kiểm. | BROWSER-MANUAL | Kết hợp nhiều lớp và nhiều request. |
| TC-FR05-HUMAN-007 | Browser search whitespace + image event sentinel; text được giữ an toàn, không image/event handler, đúng một `h1`, kết thúc ở empty state. Nửa API invariant do AI-008 kiểm. | BROWSER-MANUAL | Normalization trước DOM sink khó được sinh tự động. |
| TC-FR05-HUMAN-008 | Duplicate `search=` và SVG sentinel: status không phải 500, JSON array không phản chiếu raw sentinel, không mở rộng hơn baseline. | NEWMAN | Kết hợp HPP với security payload. |
| TC-FR05-HUMAN-009 | Browser dùng percent-encoded SQLi + script sentinel; decoded keyword chỉ là text, không script/event node, một `h1`. Nửa API decoding/differential/non-reflection do AI-012/013/015 kiểm. | BROWSER-MANUAL | Cần theo data flow từ URL decoder tới template. |
| TC-FR05-HUMAN-010 | Browser so sánh empty query và omitted query: cùng product state, keyword không phản xạ raw HTML, loading ổn định và đúng một `h1`. Nửa API equality do AI-010 kiểm. | BROWSER-MANUAL | AI gốc để semantics rỗng mơ hồ. |
