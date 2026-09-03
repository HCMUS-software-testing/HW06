# AI-Driven API Test Generator — Output Demo: FR-18 (Quản lý Đơn hàng Admin)

**Sinh viên thực hiện:** Lê Trung Kiên (MSSV: 23127075)  
**Agent Skill:** `api-test-generator`  
**Video Demo YouTube:** https://youtu.be/WtXNlbtjnk4  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` (§6.2 Quản lý Đơn hàng Admin & §4 Cart & Orders)  
**Target Requirements:** FR-18 (Quản lý đơn hàng Admin), FR-10 (Order State Machine), SEC-01..SEC-07 & RBAC  
**Target Endpoints:**
- `GET /api/admin/orders` — Xem danh sách toàn bộ đơn hàng hệ thống
- `PUT /api/admin/orders/:id/status` — Cập nhật trạng thái đơn hàng hệ thống

---

## 1. Kết Quả Thực Hiện Pipeline 6 Bước

### Bước 1: Parse Contracts & Specs
Trích xuất từ `eshop-sut/api_specification.md` và mã nguồn backend `eshop-sut/backend/server.js`:
- **GET /api/admin/orders**: Yêu cầu Header `Authorization: Bearer <token>`. Phải có `role === 'admin'`. Trả về array danh sách đơn hàng kèm thông tin user đặt hàng (`user_name`).
- **PUT /api/admin/orders/:id/status**: Yêu cầu Header `Authorization: Bearer <token>`. Phải có `role === 'admin'`. Request body JSON `{"status": "<enum_value>"}`.
- **Valid Status Enum**: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`.
- **State Machine Rules (FR-10)**:
  - Transitable: `pending` → `confirmed` | `canceled`, `confirmed` → `shipping` | `canceled`, `shipping` → `delivered`.
  - Terminal States: `delivered` (không chuyển tiếp), `canceled` (không chuyển tiếp).

### Bước 2: Domain Partitioning
Phân vùng các đầu vào:
- **Path Parameter `:id`**: Positive Integer (`1`), Zero (`0`), Negative (`-1`), String non-numeric (`abc`), Non-existent (`999999`), SQLi syntax (`1 OR 1=1`).
- **Status Field in Body**: Valid enums (`confirmed`, `shipping`, `delivered`, `canceled`), Invalid string (`unknown_status`), Missing field (`{}`), Null payload (`null`), Non-string type (`12345`), Oversized string (>1000 chars), Malformed JSON.
- **Authorization Header**: Valid Admin Token, Valid User Token (Role `user`), Missing Header, Malformed Token (`invalid_token`), Expired Token, Tampered Payload.

### Bước 3: Order State Machine Paths (FR-10)
- **Happy Paths**: `pending` → `confirmed`, `confirmed` → `shipping`, `shipping` → `delivered`, `pending` → `canceled`, `confirmed` → `canceled`.
- **Illegal Transitions (Final State & Backward)**: `delivered` → `pending`, `delivered` → `canceled`, `canceled` → `shipping`, `delivered` → `confirmed`.

### Bước 4: Security Abuse Cases (SEC-01 đến SEC-07 & RBAC)
- **RBAC Enforcement (SEC-03)**: Token có role `user` gọi API Admin bị từ chối với 403 Forbidden.
- **Authentication Enforcement (SEC-02)**: Thiếu token/Token không hợp lệ trả về 401 Unauthorized.
- **Custom Header Spoofing**: Gửi `X-Role: admin` với user token không qua mặt được backend JWT claim inspection.
- **Privilege Escalation (SEC-04/SEC-06)**: Cố ý cập nhật profile `role=admin` qua mass assignment rồi gọi API Admin.
- **SQL Injection (SEC-05)**: Payload tautology trên URL `:id` không làm sập DB hoặc lộ SQL error token.
- **XSS & Output Sanitization (SEC-07)**: Kiểm tra hiển thị `shipping_address` chứa thẻ script.

### Bước 5: Response Schema Assertions
- `GET /api/admin/orders`: 200 OK, `Content-Type: application/json`, Mảng JSON, từng item chứa các trường bắt buộc: `id` (int), `user_id` (int), `total_amount` (number), `status` (string), `shipping_address` (string), `created_at` (string), `user_name` (string).
- `PUT /api/admin/orders/:id/status`: 200 OK với body `{"message": "Order status updated"}` hoặc Error 400/401/403/404 với body `{"error": "..."}`.

### Bước 6: Deduplicate & Human Review Gate
- Loại bỏ các test case trùng lặp ngữ nghĩa dựa trên bộ nhận diện: `(Method, Endpoint, AuthMode, Payload, ExpectedOracle)`.
- Kết quả thu được **đúng 35 Candidate Test Cases** độc lập.
- **HARD GATE**: Toàn bộ 35 case được gắn nhãn `Verdict = [Manual by user]` chờ con người đánh giá (VALID / INVALID / INCOMPLETE).

---

## 2. Danh Sách Candidate Test Cases Sinh Bởi AI (35 Cases)

| STT | Case ID | Description | Method | Endpoint | Params / Request Body | Expected Status | Expected Body / Response Behavior | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC-FR18-AI-001 | Baseline list all orders with Admin Bearer Token | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | JSON Array chứa danh sách tất cả đơn hàng hệ thống | `[Manual by user]` |
| 2 | TC-FR18-AI-002 | Normal user token attempts GET admin orders (RBAC violation) | GET | `/api/admin/orders` | Header: `Bearer <userToken>` (`role='user'`) | 403 Forbidden | Từ chối truy cập do tài khoản không có quyền Admin (SEC-03) | `[Manual by user]` |
| 3 | TC-FR18-AI-003 | Missing Authorization header on GET admin orders | GET | `/api/admin/orders` | Header: *(None)* | 401 Unauthorized | Thông báo yêu cầu đăng nhập (SEC-02) | `[Manual by user]` |
| 4 | TC-FR18-AI-004 | Invalid token signature on GET admin orders | GET | `/api/admin/orders` | Header: `Bearer invalid_jwt_token_signature` | 401 / 403 | Từ chối do Token không hợp lệ hoặc sai chữ ký | `[Manual by user]` |
| 5 | TC-FR18-AI-005 | Expired JWT token on GET admin orders | GET | `/api/admin/orders` | Header: `Bearer <expiredAdminToken>` | 401 Unauthorized | Thông báo phiên đăng nhập Admin đã hết hạn | `[Manual by user]` |
| 6 | TC-FR18-AI-006 | Normal user token attempts PUT order status (Privilege Escalation) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <userToken>`<br>Body: `{"status": "confirmed"}` | 403 Forbidden | Từ chối truy cập, chỉ Admin mới có quyền cập nhật trạng thái | `[Manual by user]` |
| 7 | TC-FR18-AI-007 | Missing Authorization header on PUT order status | PUT | `/api/admin/orders/1/status` | Header: *(None)*<br>Body: `{"status": "confirmed"}` | 401 Unauthorized | Yêu cầu xác thực tài khoản Admin | `[Manual by user]` |
| 8 | TC-FR18-AI-008 | Empty Bearer token on PUT order status | PUT | `/api/admin/orders/1/status` | Header: `Bearer `<br>Body: `{"status": "confirmed"}` | 401 Unauthorized | Từ chối truy cập do Bearer Token rỗng | `[Manual by user]` |
| 9 | TC-FR18-AI-009 | Spoofed Custom Header `X-Role: admin` with normal user token | GET | `/api/admin/orders` | Header: `Bearer <userToken>`, `X-Role: admin` | 403 Forbidden | Backend chỉ đọc role từ JWT claims, không tin tưởng custom header | `[Manual by user]` |
| 10 | TC-FR18-AI-010 | Tampered JWT Payload (`role='admin'`) without valid secret re-sign | GET | `/api/admin/orders` | Header: `Bearer <tamperedJWT>` | 401 / 403 | Chữ ký không khớp với payload bị sửa đổi, từ chối truy cập | `[Manual by user]` |
| 11 | TC-FR18-AI-011 | PUT order status for non-existent order ID (`:id = 999999`) | PUT | `/api/admin/orders/999999/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 404 Not Found | Thông báo lỗi không tìm thấy đơn hàng | `[Manual by user]` |
| 12 | TC-FR18-AI-012 | PUT order status for negative order ID (`:id = -1`) | PUT | `/api/admin/orders/-1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 400 / 404 | Lỗi ID đơn hàng không hợp lệ hoặc không tìm thấy | `[Manual by user]` |
| 13 | TC-FR18-AI-013 | PUT order status for non-numeric string order ID (`:id = abc`) | PUT | `/api/admin/orders/abc/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 400 / 404 | Lỗi ID đơn hàng phải là kiểu số | `[Manual by user]` |
| 14 | TC-FR18-AI-014 | PUT order status for zero order ID (`:id = 0`) | PUT | `/api/admin/orders/0/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 404 Not Found | Thông báo lỗi đơn hàng không tồn tại | `[Manual by user]` |
| 15 | TC-FR18-AI-015 | PUT order status with missing `status` field in JSON body | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{}` | 400 Bad Request | Thông báo lỗi trường `status` là bắt buộc | `[Manual by user]` |
| 16 | TC-FR18-AI-016 | PUT order status with invalid status enum value | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "invalid_enum_val"}` | 400 Bad Request | Thông báo lỗi trạng thái không nằm trong danh mục enum hợp lệ | `[Manual by user]` |
| 17 | TC-FR18-AI-017 | PUT order status with null payload | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `null` | 400 Bad Request | Thông báo lỗi payload request không hợp lệ | `[Manual by user]` |
| 18 | TC-FR18-AI-018 | PUT order status with malformed JSON request body | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"` | 400 Bad Request | Lỗi JSON syntax parser failure | `[Manual by user]` |
| 19 | TC-FR18-AI-019 | PUT order status with extreme length status string (>1000 chars) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "a..."}` (1000+ chars) | 400 Bad Request | Từ chối chuỗi quá dài (Input boundary failure) | `[Manual by user]` |
| 20 | TC-FR18-AI-020 | PUT order status with non-string type (e.g., number) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": 12345}` | 400 Bad Request | Lỗi sai kiểu dữ liệu trường `status` | `[Manual by user]` |
| 21 | TC-FR18-AI-021 | Valid state transition: `pending` -> `confirmed` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 200 OK | Trạng thái chuyển từ `pending` sang `confirmed` thành công | `[Manual by user]` |
| 22 | TC-FR18-AI-022 | Valid state transition: `confirmed` -> `shipping` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "shipping"}` | 200 OK | Trạng thái chuyển từ `confirmed` sang `shipping` thành công | `[Manual by user]` |
| 23 | TC-FR18-AI-023 | Valid state transition: `shipping` -> `delivered` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "delivered"}` | 200 OK | Trạng thái chuyển từ `shipping` sang `delivered` thành công | `[Manual by user]` |
| 24 | TC-FR18-AI-024 | Valid state transition: `pending` -> `canceled` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` | 200 OK | Trạng thái chuyển từ `pending` sang `canceled` thành công | `[Manual by user]` |
| 25 | TC-FR18-AI-025 | Valid state transition: `confirmed` -> `canceled` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` | 200 OK | Trạng thái chuyển từ `confirmed` sang `canceled` thành công | `[Manual by user]` |
| 26 | TC-FR18-AI-026 | Illegal state transition: `delivered` -> `pending` (Final State) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "pending"}` | 400 Bad Request | Từ chối do `delivered` là trạng thái kết thúc (FR-10) | `[Manual by user]` |
| 27 | TC-FR18-AI-027 | Illegal state transition: `delivered` -> `canceled` (Final State) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "canceled"}` | 400 Bad Request | Từ chối chuyển đổi trạng thái từ đơn đã delivered | `[Manual by user]` |
| 28 | TC-FR18-AI-028 | Illegal state transition: `canceled` -> `shipping` (Final State) | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "shipping"}` | 400 Bad Request | Từ chối do `canceled` là trạng thái kết thúc (FR-10) | `[Manual by user]` |
| 29 | TC-FR18-AI-029 | Backward illegal state transition: `delivered` -> `confirmed` | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 400 Bad Request | Không cho phép chuyển ngược trạng thái từ delivered | `[Manual by user]` |
| 30 | TC-FR18-AI-030 | SQL Injection tautology probe on order `:id` path param | PUT | `/api/admin/orders/1%20OR%201=1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 400 / 404 | Từ chối ID không hợp lệ, không gây lỗi SQL syntax | `[Manual by user]` |
| 31 | TC-FR18-AI-031 | Privilege Escalation via User Profile update before Admin GET | PUT | `/api/users/me` -> `GET /api/admin/orders` | Header: `Bearer <userToken>`<br>Body: `{"role": "admin"}` | 403 Forbidden | `role` vẫn giữ nguyên là `user`, không thể tự nâng quyền | `[Manual by user]` |
| 32 | TC-FR18-AI-032 | XSS & Output Sanitization in order listing response | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | Ký tự HTML trong `shipping_address` được trả về an toàn | `[Manual by user]` |
| 33 | TC-FR18-AI-033 | Response Schema Validation for GET admin orders | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | Kiểm tra đầy đủ các trường required: `id`, `user_id`, `total_amount`, `status`, `shipping_address`, `created_at`, `user_name` | `[Manual by user]` |
| 34 | TC-FR18-AI-034 | Response Schema Validation for PUT order status | PUT | `/api/admin/orders/1/status` | Header: `Bearer <adminToken>`<br>Body: `{"status": "confirmed"}` | 200 OK | Trả về JSON chứa thuộc tính `message: "Order status updated"` | `[Manual by user]` |
| 35 | TC-FR18-AI-035 | Content-Type & Sensitive Data Leakage Check | GET | `/api/admin/orders` | Header: `Bearer <adminToken>` | 200 OK | `Content-Type: application/json; charset=utf-8`, không rò rỉ password hash hay token trong response | `[Manual by user]` |

---

## 3. Human Review Audit Table (Khung Kiểm Toán Dành Cho Người Review)

> **Hướng dẫn:** Người kiểm thử (Human Reviewer) thực hiện kiểm toán từng Candidate Case theo 3 nhãn:
> - **VALID**: Case hợp lệ, oracle đúng đặc tả.
> - **INVALID**: Case sai oracle hoặc sai endpoint spec → Cần sửa đổi hoặc EXCLUDE.
> - **INCOMPLETE**: Case thiếu fixture khởi tạo hoặc oracle chưa đủ chi tiết → Cần hoàn thiện trước khi chạy.

| ID | Verdict | Technical Reason | Final Correction / Action | Execution Class |
| --- | --- | --- | --- | --- |
| TC-FR18-AI-001 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-002 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-003 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-004 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-005 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | EXCLUDED |
| TC-FR18-AI-006 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-007 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-008 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-009 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-010 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-011 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-012 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-013 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-014 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-015 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-016 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-017 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-018 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-019 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-020 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-021 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-022 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-023 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-024 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-025 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-026 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-027 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-028 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-029 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-030 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-031 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-032 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | BROWSER-MANUAL |
| TC-FR18-AI-033 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-034 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |
| TC-FR18-AI-035 | `[Manual by user]` | `[Manual by user]` | `[Manual by user]` | NEWMAN |

---

## 4. Traceability Matrix Template

| Case ID | Final Intent | Execution Class | Postman Folder / Request Name | Assertion ID | Status Record Source |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-AI-001 | List all orders with admin token | NEWMAN | FR-18 - Admin Orders / TC-FR18-AI-001 | TC-FR18-AI-001 | `src/newman/member-2/fr-18.json` |
| TC-FR18-AI-002 | Block normal user from listing admin orders | NEWMAN | FR-18 - Admin Orders / TC-FR18-AI-002 | TC-FR18-AI-002 | `src/newman/member-2/fr-18.json` |
| TC-FR18-AI-003 | Require authentication on admin orders | NEWMAN | FR-18 - Admin Orders / TC-FR18-AI-003 | TC-FR18-AI-003 | `src/newman/member-2/fr-18.json` |
| ... | ... | ... | ... | ... | ... |
| TC-FR18-AI-035 | Verify Content-Type and no password leaks | NEWMAN | FR-18 - Admin Orders / TC-FR18-AI-035 | TC-FR18-AI-035 | `src/newman/member-2/fr-18.json` |

---

## 5. Phân Bố Test Cases Theo Danh Mục

- **RBAC & Authentication (SEC-02, SEC-03):** 10 test cases (`TC-FR18-AI-001` → `TC-FR18-AI-010`)
- **Domain Partitioning & Input Validation (SEC-01, Boundary):** 10 test cases (`TC-FR18-AI-011` → `TC-FR18-AI-020`)
- **Order State Machine Transitions (FR-10):** 9 test cases (`TC-FR18-AI-021` → `TC-FR18-AI-029`)
- **Security Abuse Cases (SEC-04..SEC-07, SQLi, Privilege Escalation, XSS):** 3 test cases (`TC-FR18-AI-030` → `TC-FR18-AI-032`)
- **Response Schema & Headers Assertions:** 3 test cases (`TC-FR18-AI-033` → `TC-FR18-AI-035`)

**Tổng số candidate cases sinh bởi AI:** 35 test cases.
