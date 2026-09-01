# Test Cases & Audit - FR-05: Liệt kê và tìm kiếm sản phẩm

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoints:**
- `GET /api/products` — Lấy danh sách sản phẩm (api_specification.md §3.1)
- `GET /api/products?search=keyword` — Tìm kiếm sản phẩm theo tên (api_specification.md §3.1)
- `GET /api/products/:id` — Xem chi tiết một sản phẩm (api_specification.md §3.2)

**Kỹ thuật:** Phân hoạch miền (Domain Partitioning)  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` §3.1–§3.2 & `eshop-sut/README.md` FR-05, FR-06

---

## 1. Danh Sách Test Cases AI Sinh & Kiểm Toán Audit

### Batch 1: Phân hoạch miền (Domain Partitioning) — 15 test cases

> **Phân vùng miền áp dụng:**
> - **GET /api/products**: Không tham số (danh sách đầy đủ)
> - **GET /api/products?search=keyword**: Từ khóa hợp lệ, từ khóa không tồn tại, từ khóa rỗng, ký tự đặc biệt, ký tự Unicode/tiếng Việt, từ khóa rất dài
> - **GET /api/products/:id**: ID tồn tại, ID = 0, ID âm, ID chuỗi ký tự, ID rất lớn, ID thiếu

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

### Bảng Kiểm Toán Audit — Batch 1

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

---

*(Batch 2: Bảo mật SQLi/XSS & Response Schema — 20 test cases sẽ được bổ sung ở prompt tiếp theo)*

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| *(Sẽ được bổ sung sau khi hoàn thành kiểm toán audit batch 1 + batch 2)* | | | | | |
