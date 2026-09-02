# Test Cases & Audit - FR-05: Liệt kê và tìm kiếm sản phẩm

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoints:**
- `GET /api/products` — Lấy danh sách sản phẩm (api_specification.md §3.1)
- `GET /api/products?search=keyword` — Tìm kiếm sản phẩm theo tên (api_specification.md §3.1)
- `GET /api/products/:id` — Xem chi tiết một sản phẩm (api_specification.md §3.2)

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

### Bảng Kiểm Toán Audit (35 Test Cases AI Sinh)

| STT | Test Case ID | Trạng thái Audit | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- |
| 1 | TC-FR05-AI-001 | [Manual by user] | [Manual by user] |
| 2 | TC-FR05-AI-002 | [Manual by user] | [Manual by user] |
| 3 | TC-FR05-AI-003 | [Manual by user] | [Manual by user] |
| 4 | TC-FR05-AI-004 | [Manual by user] | [Manual by user] |
| 5 | TC-FR05-AI-005 | [Manual by user] | [Manual by user] |
| 6 | TC-FR05-AI-006 | [Manual by user] | [Manual by user] |
| 7 | TC-FR05-AI-007 | [Manual by user] | [Manual by user] |
| 8 | TC-FR05-AI-008 | [Manual by user] | [Manual by user] |
| 9 | TC-FR05-AI-009 | [Manual by user] | [Manual by user] |
| 10 | TC-FR05-AI-010 | [Manual by user] | [Manual by user] |
| 11 | TC-FR05-AI-011 | [Manual by user] | [Manual by user] |
| 12 | TC-FR05-AI-012 | [Manual by user] | [Manual by user] |
| 13 | TC-FR05-AI-013 | [Manual by user] | [Manual by user] |
| 14 | TC-FR05-AI-014 | [Manual by user] | [Manual by user] |
| 15 | TC-FR05-AI-015 | [Manual by user] | [Manual by user] |
| 16 | TC-FR05-AI-016 | [Manual by user] | [Manual by user] |
| 17 | TC-FR05-AI-017 | [Manual by user] | [Manual by user] |
| 18 | TC-FR05-AI-018 | [Manual by user] | [Manual by user] |
| 19 | TC-FR05-AI-019 | [Manual by user] | [Manual by user] |
| 20 | TC-FR05-AI-020 | [Manual by user] | [Manual by user] |
| 21 | TC-FR05-AI-021 | [Manual by user] | [Manual by user] |
| 22 | TC-FR05-AI-022 | [Manual by user] | [Manual by user] |
| 23 | TC-FR05-AI-023 | [Manual by user] | [Manual by user] |
| 24 | TC-FR05-AI-024 | [Manual by user] | [Manual by user] |
| 25 | TC-FR05-AI-025 | [Manual by user] | [Manual by user] |
| 26 | TC-FR05-AI-026 | [Manual by user] | [Manual by user] |
| 27 | TC-FR05-AI-027 | [Manual by user] | [Manual by user] |
| 28 | TC-FR05-AI-028 | [Manual by user] | [Manual by user] |
| 29 | TC-FR05-AI-029 | [Manual by user] | [Manual by user] |
| 30 | TC-FR05-AI-030 | [Manual by user] | [Manual by user] |
| 31 | TC-FR05-AI-031 | [Manual by user] | [Manual by user] |
| 32 | TC-FR05-AI-032 | [Manual by user] | [Manual by user] |
| 33 | TC-FR05-AI-033 | [Manual by user] | [Manual by user] |
| 34 | TC-FR05-AI-034 | [Manual by user] | [Manual by user] |
| 35 | TC-FR05-AI-035 | [Manual by user] | [Manual by user] |

---

### Audit kết luận chi tiết

> Quy ước: **VALID** = mục tiêu và oracle kiểm thử được; **INCOMPLETE** = có ý đúng nhưng oracle, dữ liệu hoặc phạm vi chưa đủ; **INVALID** = không phù hợp đặc tả hoặc khẳng định sai.

| STT | Nhãn | Lý do kỹ thuật |
|---:|---|---|
| 1 | VALID | Baseline đúng endpoint; cần xác nhận schema theo đặc tả. |
| 2 | INCOMPLETE | Không chứng minh DB có `phone`; cần fixture sản phẩm chứa từ khóa và quy tắc match chính thức. |
| 3 | VALID | Empty result là hành vi hợp lệ; UI empty-state cần kiểm ở lớp frontend riêng. |
| 4 | INCOMPLETE | Cho phép đồng thời toàn bộ hoặc `[]` nên không có oracle duy nhất; phải chốt contract. |
| 5 | INCOMPLETE | Status 200 hợp lý nhưng “sản phẩm phù hợp” chưa định nghĩa; cần kiểm không crash và `[]` nếu không match. |
| 6 | INCOMPLETE | Cần fixture tên tiếng Việt và quy tắc accent/case; nếu không, không thể kết luận kết quả. |
| 7 | INCOMPLETE | Cho phép 200/400 nhưng thiếu giới hạn chính thức, status/body lỗi và đo không crash. |
| 8 | INCOMPLETE | Chưa chốt trim hay exact-match; cần contract rõ và kiểm query đã decode đúng. |
| 9 | INCOMPLETE | 200/`[]` hợp lệ nhưng thiếu oracle khi tên sản phẩm là số và quy tắc tìm kiếm. |
| 10 | VALID | ID fixture tồn tại, response object và các field bắt buộc là oracle kiểm thử được. |
| 11 | VALID | ID 0 không hợp lệ/không tồn tại; 404 phù hợp resource lookup. |
| 12 | INCOMPLETE | 400 hoặc 404 đều được chấp nhận; cần chốt validation contract. |
| 13 | INCOMPLETE | 400 hoặc 404 không đủ nhất quán để kiểm tự động; phải chọn một mã lỗi. |
| 14 | VALID | ID lớn không tồn tại có oracle 404 rõ ràng. |
| 15 | INCOMPLETE | 400/404 đều được chấp nhận; cần quy định integer validation. |
| 16 | VALID | Payload phải không biến thành tautology; kiểm thêm số lượng/kết quả baseline để phát hiện rò DB. |
| 17 | VALID | Union payload phải không truy xuất cột/bảng khác; 200 an toàn hoặc 400 đều có thể chấp nhận. |
| 18 | INCOMPLETE | Ngưỡng `<1s` phụ thuộc môi trường; cần baseline/timeout và xác nhận DB PostgreSQL trước khi dùng `pg_sleep`. |
| 19 | VALID | Kiểm đúng chống phá câu SQL và không 500; nên kiểm response schema nữa. |
| 20 | INCOMPLETE | API JSON không tự render HTML; phải kiểm UI sink/DOM, không chỉ yêu cầu `[]`. |
| 21 | INCOMPLETE | Tương tự TC20; sanitize thuộc response không được định nghĩa và XSS cần kiểm ở consumer. |
| 22 | INCOMPLETE | `javascript:` không phải XSS nếu chỉ là query; cần kiểm URL/DOM sink cụ thể. |
| 23 | INCOMPLETE | 200/400 quá rộng; thiếu giới hạn, timeout, body lỗi và giới hạn tài nguyên. |
| 24 | INCOMPLETE | Null byte trong query không lộ file là oracle lệch ngữ cảnh; cần xác định expected search/error và không 500. |
| 25 | VALID | Kiểm UTF-8, status 200, JSON hợp lệ và không crash; kết quả `[]` cần fixture xác nhận. |
| 26 | VALID | Kiểm integer JSON là assertion schema rõ ràng trên danh sách. |
| 27 | VALID | Kiểm string không rỗng là assertion hợp lệ nếu đặc tả bắt buộc name. |
| 28 | VALID | Kiểm number dương phù hợp invariant giá sản phẩm. |
| 29 | VALID | Kiểm kiểu string đúng theo schema. |
| 30 | VALID | Kiểm kiểu string đúng theo schema; nên bổ sung URL format nếu contract yêu cầu. |
| 31 | VALID | Kiểm integer category_id đúng schema; cần xử lý sản phẩm không có category nếu được phép. |
| 32 | INCOMPLETE | “Chính xác 6 thuộc tính” quá cứng nếu API cho phép metadata; cần phân biệt required và additional fields. |
| 33 | VALID | Content-Type JSON là header contract kiểm tự động được. |
| 34 | VALID | Empty state array và length 0 là oracle rõ với keyword fixture không tồn tại. |
| 35 | INCOMPLETE | Danh sách field nhạy cảm chưa theo data contract; cần allowlist/denylist chính thức và kiểm đệ quy. |

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| TC-FR05-HUMAN-001 | SQLi Blind Boolean-based qua tham số search | Bảo mật (SEC-05) | `GET /api/products?search=phone' AND 1=1--` vs `search=phone' AND 1=2--` | Cả 2 request đều trả về kết quả giống nhau (không rò rỉ boolean SQL injection) | AI thường bỏ sót các kỹ thuật Blind SQLi phức tạp cần so sánh 2 kết quả phản hồi |
| TC-FR05-HUMAN-002 | Reflected XSS trong thẻ H1/Empty State UI rendering | Bảo mật (SEC-04) | `GET /api/products?search=<svg/onload=alert(1)>` | Response JSON được escape an toàn; UI khi nhận JSON không thi hành SVG script | AI chỉ chú ý đến JSON response mà không đánh giá ngữ cảnh render UI của empty state (README FR-05) |
| TC-FR05-HUMAN-003 | Parameter Pollution (HPP) trên query `search` | Edge / Security | `GET /api/products?search=phone&search=laptop` | Server xử lý tham số đầu tiên hoặc ghép nối hợp lý, không ném ngoại lệ 500 | AI ít khi kiểm thử việc truyền trùng lặp tên query parameter (HTTP Parameter Pollution) |
| TC-FR05-HUMAN-004 | Lấy sản phẩm với ID dạng Hexadecimal / Path Traversal | Bảo mật / Path | `GET /api/products/0x1` hoặc `GET /api/products/..%2f1` | Trả về 400 Bad Request hoặc 404 Not Found | AI bỏ sót kết hợp giữa mã hóa URL Hexadecimal và Path Traversal trong đường dẫn URL |
| TC-FR05-HUMAN-005 | Kiểm tra tính nhất quán giữa danh sách và chi tiết sản phẩm | Data Integrity | 1. Gọi `GET /api/products`<br>2. Lấy `price`, `name` của product ID=1<br>3. Gọi `GET /api/products/1` và so sánh | Thông tin `name`, `price`, `category_id` khớp chính xác 100% giữa 2 endpoint | AI sinh testcase đơn lẻ cho từng endpoint mà không kết hợp liên kết dữ liệu giữa 2 API trong cùng FR |

### Bổ sung human-designed tập trung vào kết hợp search rỗng, SQLi và HTML safety

| ID | Kịch bản và cách thực hiện | Expected result | Vì sao AI thường bỏ sót |
|---|---|---|---|
| TC-FR05-HUMAN-006 | Gửi `search=` rồi render empty state; lặp với `search=' OR '1'='1` | Không mở rộng kết quả; UI escape text, không tạo HTML/script; không 500 | AI tách security khỏi UI và không theo dõi dữ liệu qua nhiều lớp. |
| TC-FR05-HUMAN-007 | Gửi `search=   <img src=x onerror=alert(1)>   ` sau trim | Kết quả/empty state nhất quán; payload chỉ là text, không event thực thi | AI thường kiểm payload nguyên dạng, bỏ qua biến thể whitespace + normalization. |
| TC-FR05-HUMAN-008 | Gửi đồng thời `search=&search=<svg/onload=alert(1)>` | Server có quy tắc duplicate rõ; không SQLi/XSS và không phản hồi 500 | AI ít sinh HPP kết hợp payload với empty value. |
| TC-FR05-HUMAN-009 | Gửi `search=%27%20OR%201%3D1--%3Cscript%3E` rồi đưa response vào template HTML | Không trả toàn bộ DB; DOM không có node script/event handler | AI dừng ở HTTP response, không kiểm tra sink và URL decoding. |
| TC-FR05-HUMAN-010 | So sánh `/products?search=` với `/products` và kiểm escape chuỗi tìm kiếm trong empty-state | Semantics đã chốt (thường cùng baseline); không phản xạ raw query vào HTML | AI cho phép nhiều expected result nên bỏ sót regression giữa baseline và rendering. |
