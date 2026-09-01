# AI Audit Report

## 1. Thông tin nhóm

- Họ tên: `Lê Trung Kiên`
- MSSV: `23127075`
- Nhóm/Lớp: `[TODO]`

## 2. Bảng audit

### 2.1. Tóm tắt audit

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |
| 1 | Time: `2026-09-01 21:58 +07`<br>Tool: `Gemini 3.6 Flash / Antigravity`<br>Prompt:<br>1. Tôi là thành viên 2, Lê Trung Kiên, mã số sinh viên 23127075. Hãy note lại và note vào cả 2 file markdown trong docs<br>2. Cập nhật rules đọc folder req ưu tiên đọc markdown trước.<br>3. /writing-skills Cập nhật skill /ai-audit-entry để phù hợp với project hiện tại. Biết rằng folder src sẽ được copy ra và đổi tên lại thành folder nộp. Nên folder src chính là folder làm bài chính. | [Manual by user] |
| 2 | Time: `2026-09-01 22:00 +07`<br>Tool: `Gemini 3.6 Flash / Antigravity`<br>Prompt:<br>/using-superpowers Đọc folder req (đề) để setup folder src (chỉ cần template thôi, chưa cần làm). Sau đó tạo spec và plan để tôi hoàn thành 10 điểm bài tập này. | [Manual by user] |
| 3 | Time: `2026-09-01 23:01 +07`<br>Tool: `Claude Opus 4.6 / Antigravity`<br>Prompt:<br>/using-superpowers Đọc đề trong folder req, eshop-sut/README.md và eshop-sut/api_specification.md, hãy giúp tôi viết Pre-request Script cho Postman Collection HW06_API_Testing. Mục tiêu là tự động chèn header 'X-Student-Id: 23127075' vào mọi HTTP request trước khi gửi đi. Đồng thời hãy tạo cấu trúc JSON cho Postman Environment file với các biến chính thức từ eshop-sut: baseUrl (http://localhost:3000), studentId (23127075), userToken, adminToken. | [Manual by user] |
| 4 | Time: `2026-09-01 23:04 +07`<br>Tool: `Claude Opus 4.6 / Antigravity`<br>Prompt:<br>/using-superpowers Dựa vào đặc tả API FR-05 trong eshop-sut/api_specification.md cho các endpoint GET /api/products và GET /api/products?search=keyword, hãy sinh 15 test cases bao phủ kỹ thuật Phân hoạch miền (Domain Partitioning) trên các tham số: query search (tìm từ khóa hợp lệ, từ khóa không tồn tại, từ khóa rỗng, ký tự đặc biệt), phân trang (nếu có), và lấy chi tiết sản phẩm GET /api/products/:id (id tồn tại, id=0, id âm, id chuỗi). Định dạng output dạng bảng gồm: STT, Test Case Name, Method, Endpoint, Query/Path Params, Expected Status, Expected Schema/Body. | [Manual by user] |
| 5 | Time: `2026-09-01 23:08 +07`<br>Tool: `Gemini 3.6 Flash / Antigravity`<br>Prompt:<br>/using-superpowers Tiếp tục với API FR-05 (GET /api/products?search=keyword), hãy sinh 20 test cases tập trung vào 2 khía cạnh: 1. Bảo mật (SEC-01 đến SEC-07): SQL Injection trong tham số tìm kiếm 'search' (ví dụ: ' OR '1'='1, UNION SELECT), XSS payload (<script>alert(1)</script>), tham số quá dài (>255 chars), ký tự đặc biệt UTF-8/Unicode. 2. Response Schema Validation: Kiểm tra cấu trúc JSON trả về khớp với eshop-sut (danh sách sản phẩm chứa id, name, price, description, imageUrl, category_id), kiểm tra type của từng thuộc tính (id: integer, price: number > 0). Định dạng dạng bảng chi tiết. | [Manual by user] |

### 2.2. Chi tiết audit

### 2.2.1 Entry 1

**Prompt + Tool:**
Time: `2026-09-01 21:58 +07`
Tool: `Gemini 3.6 Flash / Antigravity`
Prompt:
1. Tôi là thành viên 2, Lê Trung Kiên, mã số sinh viên 23127075. Hãy note lại và note vào cả 2 file markdown trong docs
2. Cập nhật rules đọc folder req ưu tiên đọc markdown trước.
3. /writing-skills Cập nhật skill /ai-audit-entry để phù hợp với project hiện tại. Biết rằng folder src sẽ được copy ra và đổi tên lại thành folder nộp. Nên folder src chính là folder làm bài chính.

**AI Output:** Đã cập nhật thông tin Lê Trung Kiên - 23127075 vào docs/hw06-phan-cong-cong-viec-nhom.md và docs/hw06-team-task-allocation.md. Đã tạo file quy tắc .agents/AGENTS.md quy định ưu tiên đọc file markdown trong req/. Đã cập nhật skill .agents/skills/ai-audit-entry/SKILL.md theo chuẩn writing-skills và quy định src/ là thư mục làm bài chính.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.2 Entry 2

**Prompt + Tool:**
Time: `2026-09-01 22:00 +07`
Tool: `Gemini 3.6 Flash / Antigravity`
Prompt:
/using-superpowers Đọc folder req (đề) để setup folder src (chỉ cần template thôi, chưa cần làm). Sau đó tạo spec và plan để tôi hoàn thành 10 điểm bài tập này.

**AI Output:** Đã đọc file đề bài req/2026.HW06.API Testing_Vi.md, dựng toàn bộ khung thư mục và file mẫu (templates) trong src/ (bao gồm README self-assessment, docs, postman, newman, test-cases, bug-reports, agent-skill), và lập hồ sơ đặc tả Spec (docs/superpowers/specs/2026-09-01-hw06-api-testing-spec.md) cùng Kế hoạch thực hiện Plan (docs/superpowers/plans/2026-09-01-hw06-api-testing-plan.md) để đạt 100/100 điểm.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.3 Entry 3

**Prompt + Tool:**
Time: `2026-09-01 23:01 +07`
Tool: `Claude Opus 4.6 / Antigravity`
Prompt:
/using-superpowers Đọc đề trong folder req, eshop-sut/README.md và eshop-sut/api_specification.md, hãy giúp tôi viết Pre-request Script cho Postman Collection HW06_API_Testing. Mục tiêu là tự động chèn header 'X-Student-Id: 23127075' vào mọi HTTP request trước khi gửi đi. Đồng thời hãy tạo cấu trúc JSON cho Postman Environment file với các biến chính thức từ eshop-sut: baseUrl (http://localhost:3000), studentId (23127075), userToken, adminToken.

**AI Output:** Đã tạo/cập nhật 2 file dựa trên đặc tả chính thức eshop-sut/api_specification.md và eshop-sut/README.md: (1) src/postman/HW06_API_Testing.postman_collection.json — Collection Postman v2.1 với collection-level pre-request script dùng pm.request.headers.upsert() để chèn header X-Student-Id: 23127075 vào mọi request (tránh duplicate bằng upsert thay vì add), console.log ghi method + URL phục vụ screenshot chống gian lận §11, collection-level test script kiểm tra response time < 5s và valid JSON, 4 folders (00-Setup Auth với auto-save userToken/adminToken, Pool A FR-05, Pool B FR-08, Pool C FR-18), mỗi request có test assertions riêng. (2) src/postman/HW06_Local.postman_environment.json — 9 biến environment: baseUrl=http://localhost:3000, studentId=23127075, userToken/adminToken (type: secret, auto-populated bởi login requests), lastOrderId (chaining FR-08→FR-18), userEmail/userPassword/adminEmail/adminPassword từ tài khoản mặc định eshop-sut/README.md.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.4 Entry 4

**Prompt + Tool:**
Time: `2026-09-01 23:04 +07`
Tool: `Claude Opus 4.6 / Antigravity`
Prompt:
/using-superpowers Dựa vào đặc tả API FR-05 trong eshop-sut/api_specification.md cho các endpoint GET /api/products và GET /api/products?search=keyword, hãy sinh 15 test cases bao phủ kỹ thuật Phân hoạch miền (Domain Partitioning) trên các tham số: query search (tìm từ khóa hợp lệ, từ khóa không tồn tại, từ khóa rỗng, ký tự đặc biệt), phân trang (nếu có), và lấy chi tiết sản phẩm GET /api/products/:id (id tồn tại, id=0, id âm, id chuỗi). Định dạng output dạng bảng gồm: STT, Test Case Name, Method, Endpoint, Query/Path Params, Expected Status, Expected Schema/Body.

**AI Output:** Đã sinh 15 test cases FR-05 theo kỹ thuật Phân hoạch miền vào file src/test-cases/member-2-fr-05.md. Phân vùng bao gồm: (A) GET /api/products không tham số (1 case), (B) GET /api/products?search=keyword — từ khóa hợp lệ, không tồn tại, rỗng, ký tự đặc biệt ASCII, Unicode tiếng Việt, dài > 255 ký tự, khoảng trắng, chữ số (8 cases), (C) GET /api/products/:id — id tồn tại, id=0, id âm, id chuỗi, id rất lớn, id thập phân (6 cases). Mỗi test case có đầy đủ: Method, Endpoint, Query/Path Params, Expected Status, Expected Schema/Body. Bảng kiểm toán audit để trống cho sinh viên tự đánh giá.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.5 Entry 5

**Prompt + Tool:**
Time: `2026-09-01 23:08 +07`
Tool: `Gemini 3.6 Flash / Antigravity`
Prompt:
/using-superpowers Tiếp tục với API FR-05 (GET /api/products?search=keyword), hãy sinh 20 test cases tập trung vào 2 khía cạnh:
1. Bảo mật (SEC-01 đến SEC-07): SQL Injection trong tham số tìm kiếm 'search' (ví dụ: ' OR '1'='1, UNION SELECT), XSS payload (<script>alert(1)</script>), tham số quá dài (>255 chars), ký tự đặc biệt UTF-8/Unicode.
2. Response Schema Validation: Kiểm tra cấu trúc JSON trả về khớp với eshop-sut (danh sách sản phẩm chứa id, name, price, description, imageUrl, category_id), kiểm tra type của từng thuộc tính (id: integer, price: number > 0).
Định dạng dạng bảng chi tiết.

**AI Output:** Đã bổ sung 20 test cases Batch 2 (Bảo mật SQLi/XSS & Response Schema Validation, nâng tổng số test cases do AI sinh lên 35 cases) và bổ sung 5 test cases do con người thiết kế (Human-designed) vào file src/test-cases/member-2-fr-05.md. Các case bảo mật gồm: SQLi Tautology, Union, Time Delay, Comment out; Reflected XSS Script, Img onerror, Javascript pseudo-protocol; Oversized buffer (5000 chars), Null byte, Emojis. Các case schema gồm: type validation của id, name, price (>0), description, imageUrl, category_id, 6-field detail object, Content-Type application/json, Empty state array [], và không rò rỉ secret field. 5 Human cases gồm: Blind SQLi Boolean, Reflected XSS UI rendering empty state, HTTP Parameter Pollution, Path Traversal/Hex ID, và Data Integrity Consistency giữa list & detail API.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

## 3. Tổng kết độ chính xác AI

- Các nội dung AI tạo đã được rà soát với yêu cầu bài làm: `[TODO]`
- Mức độ chính xác/độ hữu ích tổng quan: `[TODO]`
- Giới hạn hoặc rủi ro còn lại: `[TODO]`

## 4. Kết luận

`[TODO]`

## 5. Disclosure

`[TODO]`
