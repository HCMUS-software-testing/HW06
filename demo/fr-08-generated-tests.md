# AI-Generated API Test Cases Demo — FR-08 (Checkout)

> **Skill được sử dụng:** `.agents/skills/api-test-generator/SKILL.md`  
> **Nguồn đặc tả:** `eshop-sut/api_specification.md` §3.4 & `eshop-sut/README.md` (FR-08 Checkout)  
> **Thời gian thực thi:** 2026-09-03  
> **Trạng thái:** Chờ Human Review Gate (Tất cả Verdicts để `[Manual by user]`)

---

## 1. Danh Sách Candidate Test Cases do AI Sinh (35 Test Cases)

| STT | Case ID | Description | Method | Endpoint | Request Body / Params | Expected Status | Expected Body / Schema Assertion | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC-FR08-AI-001 | Checkout thành công với giỏ hàng hợp lệ và địa chỉ chuẩn | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi, TP.HCM"}` | 200 OK | `{"message": "Checkout successful", "orderId": number}`; cart rỗng sau checkout | [Manual by user] |
| 2 | TC-FR08-AI-002 | Checkout khi giỏ hàng rỗng | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi"}` | 400 Bad Request | JSON error message "Cart is empty" | [Manual by user] |
| 3 | TC-FR08-AI-003 | Checkout khi chưa đăng nhập (Thiếu Token) | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi"}` | 401 Unauthorized | JSON error message "Unauthorized" | [Manual by user] |
| 4 | TC-FR08-AI-004 | Checkout với địa chỉ giao hàng là chuỗi rỗng `""` | POST | `/api/checkout` | `{"shipping_address": ""}` | 400 Bad Request | JSON error message validation error | [Manual by user] |
| 5 | TC-FR08-AI-005 | Checkout với địa chỉ chỉ chứa khoảng trắng `"   "` | POST | `/api/checkout` | `{"shipping_address": "   "}` | 400 Bad Request | JSON error validation error | [Manual by user] |
| 6 | TC-FR08-AI-006 | Checkout khi thiếu trường `shipping_address` | POST | `/api/checkout` | `{}` | 400 Bad Request | JSON validation error | [Manual by user] |
| 7 | TC-FR08-AI-007 | Checkout với `shipping_address = null` | POST | `/api/checkout` | `{"shipping_address": null}` | 400 Bad Request | JSON validation error | [Manual by user] |
| 8 | TC-FR08-AI-008 | Checkout với `shipping_address` dạng Object | POST | `/api/checkout` | `{"shipping_address": {"street": "123"}}` | 400 Bad Request | JSON validation error | [Manual by user] |
| 9 | TC-FR08-AI-009 | Checkout khi client tự truyền `total_amount` thao túng giá | POST | `/api/checkout` | `{"total_amount": 1, "shipping_address": "123 Le Loi"}` | 200 OK / 400 | Server phải tự tính lại tổng tiền từ giỏ hàng, KHÔNG tin giá trị client | [Manual by user] |
| 10 | TC-FR08-AI-010 | Checkout với JWT Token không hợp lệ / giả mạo | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi"}` | 401 / 403 | Access denied | [Manual by user] |
| 11 | TC-FR08-AI-011 | Checkout với JWT Token hết hạn (Expired) | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi"}` | 401 Unauthorized | Token expired error | [Manual by user] |
| 12 | TC-FR08-AI-012 | Checkout với địa chỉ chứa ký tự đặc biệt ASCII | POST | `/api/checkout` | `{"shipping_address": "!@#$%^&*()"}` | 200 OK / 400 | Trả kết quả an toàn, KHÔNG crash 500 | [Manual by user] |
| 13 | TC-FR08-AI-013 | Checkout với địa chỉ tiếng Việt Unicode UTF-8 | POST | `/api/checkout` | `{"shipping_address": "123 Đường Nguyễn Trãi, Quận 1"}` | 200 OK | Đơn hàng tạo thành công với địa chỉ UTF-8 chuẩn | [Manual by user] |
| 14 | TC-FR08-AI-014 | Checkout với địa chỉ cực dài (> 1000 ký tự) | POST | `/api/checkout` | `{"shipping_address": "A".repeat(1000)}` | 400 / 200 | Xử lý an toàn, KHÔNG crash Buffer Overflow | [Manual by user] |
| 15 | TC-FR08-AI-015 | SQL Injection probe trong `shipping_address` | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi' OR '1'='1"}` | 200 OK | Trích xuất dạng literal string, KHÔNG bị lỗi SQL syntax | [Manual by user] |
| 16 | TC-FR08-AI-016 | Reflected XSS probe trong `shipping_address` | POST | `/api/checkout` | `{"shipping_address": "<script>alert('xss')</script>"}` | 200 OK | Lưu dạng text an toàn, KHÔNG thực thi script | [Manual by user] |
| 17 | TC-FR08-AI-017 | Schema Check: Trạng thái đơn hàng khởi tạo | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi"}` | 200 OK | Trạng thái đơn tạo ra trong DB phải là `"pending"` | [Manual by user] |
| 18 | TC-FR08-AI-018 | Response Header Check: Content-Type JSON | POST | `/api/checkout` | `{"shipping_address": "123 Le Loi"}` | 200 OK | Response header `Content-Type` chứa `application/json` | [Manual by user] |

*(Danh sách 35 cases hoàn chỉnh trích từ pipeline 6 bước của Agent Skill)*

---

## 2. Bảng Kiểm Toán Audit (Mẫu sau Human Gate)

| ID | Verdict | Technical Reason | Final Correction | Execution Class |
| --- | --- | --- | --- | --- |
| TC-FR08-AI-001 | VALID | Đơn hàng tạo thành công với cart có sản phẩm | POST `/api/checkout`; check 200 OK và cart bị xóa | NEWMAN |
| TC-FR08-AI-002 | VALID | Đúng quy tắc nghiệp vụ: cart rỗng phải reject | Check status 400 Bad Request | NEWMAN |
| TC-FR08-AI-009 | INVALID | AI giả định backend sẽ reject `total_amount` client | SUT thực tế bị BUG-002: lưu giá trị client 1 VND | NEWMAN |

---

## 3. Ma Trận Định Tuyến Traceability Matrix

| Case ID | Final Intent | Execution Class | Postman Request | Assertion ID | Result Target |
| --- | --- | --- | --- | --- | --- |
| TC-FR08-AI-001 | Successful checkout clears cart | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-001` | TC-FR08-AI-001 | `src/newman/member-2/fr-08.json` |
| TC-FR08-AI-002 | Empty cart rejected | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-002` | TC-FR08-AI-002 | `src/newman/member-2/fr-08.json` |
