# Danh Sách Prompt Chuẩn Bị Cho AI Audit Report (Dựa Trên đặc tả eshop-sut)

**Sinh viên:** Lê Trung Kiên (MSSV: 23127075) - Thành viên 2  
**Đặc tả chuẩn SUT:** `eshop-sut/api_specification.md` & `eshop-sut/README.md` (Port backend: `http://localhost:3000`)  
**Mục đích:** Cung cấp bộ prompt được cấu trúc từng bước (step-by-step disciplined prompting) theo từng Task trong `IMPLEMENTATION_PLAN.md`. Mỗi prompt tương ứng với một lượt ghi nhận trong **Báo cáo Kiểm toán AI (`src/ai-audit/ai_audit_report.md`)**.

---

## Task 0: Thiết Lập Dự Án & Skill Audit
### Prompt 0.1 (Entry 1)
```text
1. Tôi là thành viên 2, Lê Trung Kiên, mã số sinh viên 23127075. Hãy note lại và note vào cả 2 file markdown trong docs
2. Cập nhật rules đọc folder req ưu tiên đọc markdown trước.
3. /writing-skills Cập nhật skill /ai-audit-entry để phù hợp với project hiện tại. Biết rằng folder src sẽ được copy ra và đổi tên lại thành folder nộp. Nên folder src chính là folder làm bài chính.
```

### Prompt 0.2 (Entry 2)
```text
/using-superpowers Đọc folder req (đề) để setup folder src (chỉ cần template thôi, chưa cần làm). Sau đó tạo spec và plan để tôi hoàn thành 10 điểm bài tập này.
```

---

## Task 1: Thiết Lập Hạ Tầng Postman Collection & Pre-request Script
### Prompt 1.1 (Entry 3)
```text
/using-superpowers Đọc đề trong folder req, eshop-sut/README.md và eshop-sut/api_specification.md, hãy giúp tôi viết Pre-request Script cho Postman Collection HW06_API_Testing. Mục tiêu là tự động chèn header 'X-Student-Id: 23127075' vào mọi HTTP request trước khi gửi đi. Đồng thời hãy tạo cấu trúc JSON cho Postman Environment file với các biến chính thức từ eshop-sut: baseUrl (http://localhost:3000), studentId (23127075), userToken, adminToken.
```

---

## Task 2: Pipeline API 1 - FR-05 (Liệt Kê Và Tìm Kiếm Sản Phẩm)
### Prompt 2.1 (Entry 4): Phân Hoạch Miền
```text
/using-superpowers Dựa vào đặc tả API FR-05 trong eshop-sut/api_specification.md cho các endpoint GET /api/products và GET /api/products?search=keyword, hãy sinh 15 test cases bao phủ kỹ thuật Phân hoạch miền (Domain Partitioning) trên các tham số: query search (tìm từ khóa hợp lệ, từ khóa không tồn tại, từ khóa rỗng, ký tự đặc biệt), phân trang (nếu có), và lấy chi tiết sản phẩm GET /api/products/:id (id tồn tại, id=0, id âm, id chuỗi). Định dạng output dạng bảng gồm: STT, Test Case Name, Method, Endpoint, Query/Path Params, Expected Status, Expected Schema/Body.
```

### Prompt 2.2 (Entry 5): Bảo Mật & Response Schema
```text
/using-superpowers Tiếp tục với API FR-05 (GET /api/products?search=keyword), hãy sinh 20 test cases tập trung vào 2 khía cạnh:
1. Bảo mật (SEC-01 đến SEC-07): SQL Injection trong tham số tìm kiếm 'search' (ví dụ: ' OR '1'='1, UNION SELECT), XSS payload (<script>alert(1)</script>), tham số quá dài (>255 chars), ký tự đặc biệt UTF-8/Unicode.
2. Response Schema Validation: Kiểm tra cấu trúc JSON trả về khớp với eshop-sut (danh sách sản phẩm chứa id, name, price, description, imageUrl, category_id), kiểm tra type của từng thuộc tính (id: integer, price: number > 0).
Định dạng dạng bảng chi tiết.
```

---

## Task 3: Pipeline API 2 - FR-08 (Thanh Toán / Tạo Đơn Hàng)
### Prompt 3.1 (Entry 6): Luồng Nghiệp Vụ Checkout
```text
/using-superpowers Dựa vào đặc tả API FR-08 POST /api/checkout trong eshop-sut/api_specification.md, hãy sinh 18 test cases kiểm thử các luồng nghiệp vụ tạo đơn hàng: checkout hợp lệ với JSON body {"total_amount": 200000, "shipping_address": "123 Le Loi, TP.HCM"}, checkout khi giỏ hàng rỗng, checkout với số lượng sản phẩm vượt quá tồn kho (out of stock), checkout với thông tin địa chỉ giao hàng không hợp lệ (thiếu street, phone sai định dạng, name rỗng), và checkout khi áp dụng mã giảm giá coupon. Output dạng bảng với thông tin chi tiết request body và expected result.
```

### Prompt 3.2 (Entry 7): Xác Thực & Schema Boundary
```text
/using-superpowers Tiếp tục với API FR-08 POST /api/checkout, hãy sinh 17 test cases kiểm thử:
1. Bảo mật & Xác thực: Checkout khi chưa đăng nhập (không gửi Authorization: Bearer <token> header), checkout với Token hết hạn / không hợp lệ, checkout sử dụng Token của user khác (IDOR trên giỏ hàng).
2. Response Schema & Boundary: Payload JSON bị lỗi cú pháp, dư thừa trường không xác định, kiểm tra response JSON trả về chứa order_id, order_status='pending', total_amount khớp tính toán.
Format kết quả dạng bảng.
```

---

## Task 4: Pipeline API 3 - FR-18 (Quản Lý Đơn Hàng Admin)
### Prompt 4.1 (Entry 8): Phân Quyền RBAC
```text
/using-superpowers Dựa vào đặc tả API FR-18 trong eshop-sut cho Admin (GET /api/admin/orders và PUT /api/admin/orders/:id/status), hãy sinh 18 test cases kiểm thử:
1. Quyền truy cập Admin: Truy cập GET /api/admin/orders với Admin Token hợp lệ (role='admin'), kiểm tra danh sách tất cả đơn hàng hệ thống.
2. Kiểm soát truy cập RBAC (SEC-04): Cố gắng truy cập endpoint Admin bằng User Token (role user thường) -> Kỳ vọng 403 Forbidden; truy cập không có token -> 401 Unauthorized.
Format bảng chi tiết.
```

### Prompt 4.2 (Entry 9): Máy Trạng Thái Đơn Hàng & Path Params
```text
/using-superpowers Tiếp tục với API FR-18 PUT /api/admin/orders/:id/status (Body: {"status": "confirmed"}), hãy sinh 17 test cases kiểm thử Máy trạng thái đơn hàng (State Machine FR-10):
1. Chuyển trạng thái hợp lệ: pending -> confirmed -> shipping -> delivered.
2. Chuyển trạng thái KHÔNG hợp lệ (Invalid transitions): delivered -> pending, canceled -> shipping, delivered -> canceled (vì delivered và canceled là các trạng thái kết thúc final states).
3. IDOR & Path Parameter: Update status cho order_id không tồn tại (404), order_id âm hoặc chuỗi ký tự (400), IDOR vào đơn hàng thuộc tenant khác.
Format bảng chi tiết.
```

---

## Task 5: Audit 105 AI Cases & Gợi Ý Human-Designed Cases
### Prompt 5.1 (Entry 10)
```text
Thực hiện đồng thời 3 task sau:
1. Tôi có bộ 35 test cases FR-05 do AI sinh. Hãy giúp tôi đánh giá và gán nhãn từng test case là VALID, INVALID hoặc INCOMPLETE kèm lý do kỹ thuật. Sau đó, gợi ý 5 test cases do con người tự thiết kế (Human-designed) mà AI thường bỏ sót cho API FR-05 (đặc biệt là các case kết hợp giữa tìm kiếm rỗng + SQLi + HTML rendering safety) và giải thích tại sao AI bỏ sót chúng.
2. Hãy giúp tôi kiểm toán toàn bộ 35 test cases FR-08 do AI sinh ra (gán nhãn VALID/INVALID/INCOMPLETE kèm lý do). Sau đó, hãy gợi ý 5 test cases quan trọng về Race Condition và Thay đổi Trạng thái Đa phiên (ví dụ: checkout đúng lúc giỏ hàng bị rỗng ở tab khác, tồn kho bị giảm về 0 ngay trước thời điểm bấm thanh toán) mà AI thường bỏ sót và giải thích nguyên nhân AI bỏ sót.
3. Hãy kiểm toán 35 test cases FR-18 do AI sinh (VALID/INVALID/INCOMPLETE + lý do). Gợi ý 5 test cases do con người tự bổ sung tập trung vào Privilege Escalation (người dùng tự sửa role để gọi API Admin status) và Rollback trạng thái khi gặp sự cố hệ thống mà AI bỏ sót, giải thích nguyên nhân.
Có ghi audit cho lần prompt này.
```

---

## Task 6: Agent Skill - AI Test Generator Design
### Prompt 6.1 (Entry 11)
```text
Tôi đang thiết kế một Agent Skill tự động sinh test cases API từ đặc tả OpenAPI/Markdown của EShop cho bài tập HW06. Hãy giúp tôi viết mã giả (Pseudocode) bằng Python thể hiện pipeline 4 giai đoạn sinh thử nghiệm: (1) Domain Partitioning, (2) State Machine Transitions (pending/confirmed/shipping/delivered/canceled), (3) Security SEC-01..07 & RBAC, (4) Response Schema Validation; sau đó tự động deduplicate và xuất ra Postman Collection format.
```

---

## Task 7: Tích Hợp CI/CD Workflow
### Prompt 7.1 (Entry 12): Workflow GitHub Actions
```text
Hãy viết một file GitHub Actions workflow (.github/workflows/newman-api-tests.yml) để tự động chạy Postman Collection bằng Newman trên môi trường Ubuntu Latest. Workflow cần: checkout repo, khởi chạy SUT (Node.js backend tại port 3000), install newman và newman-reporter-htmlextra, chạy collection với file environment, và upload Newman HTML report làm Artifact.
```

---

## Task 8: Tự Động Hóa Thực Thi Newman & Ma Trận Định Tuyến Traceability
### Prompt 8.1 (Entry 13): Runner Newman & Traceability
```text
Hãy giúp tôi thiết lập script chạy Newman tự động cho cả 3 bộ API (FR-05, FR-08, FR-18), tạo data fixture JSON cho từng FR, ghi nhận kết quả thực thi vào src/newman/member-2/ (file json, html, txt, summary.json), đồng thời tổng hợp ma trận định tuyến kiểm thử src/test-cases/member-2-traceability.md và Báo cáo lỗi kỹ thuật src/bug-reports/member-2-bugs.md.
```
