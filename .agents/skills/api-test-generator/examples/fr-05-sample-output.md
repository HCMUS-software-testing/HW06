# Ví dụ Output — FR-05: Liệt kê và tìm kiếm sản phẩm

Dưới đây là 5 case mẫu minh họa format output kỳ vọng khi chạy skill `api-test-generator` cho FR-05.

## Test Cases sinh bởi AI (mẫu 5/35)

| STT | Case ID | Description | Method | Endpoint | Params/Body | Expected Status | Expected Body | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC-FR05-AI-001 | Baseline list trả 200 JSON array với đầy đủ product fields | GET | /api/products | (none) | 200 | JSON array; mỗi phần tử có `id`, `name`, `price`, `description`, `imageUrl`, `category_id` | [Manual by user] |
| 2 | TC-FR05-AI-002 | Tìm kiếm với từ khóa fixture tồn tại trong DB | GET | /api/products | ?search={dynamicKeyword} | 200 | JSON array ≥1 phần tử, mọi `name` chứa keyword | [Manual by user] |
| 3 | TC-FR05-AI-003 | Tìm kiếm sentinel không tồn tại trả mảng rỗng | GET | /api/products | ?search=xyznonexistent999 | 200 | `[]` (empty JSON array) | [Manual by user] |
| 4 | TC-FR05-AI-016 | SQL Injection tautology không mở rộng kết quả | GET | /api/products | ?search=' OR '1'='1 | 200 | JSON array, cardinality ≤ baseline, không SQL error token | [Manual by user] |
| 5 | TC-FR05-AI-026 | Schema: mỗi product `id` là positive integer | GET | /api/products | (none) | 200 | Mọi `id` thỏa `typeof === 'number'` và `Number.isInteger()` | [Manual by user] |

## Audit Table mẫu (sau khi human review)

| ID | Verdict | Technical reason | Final correction | Execution class |
| --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | VALID | Đúng endpoint list và có schema quan sát được. | Gọi không query; 200, `application/json`, body là array; mọi phần tử có required fields. | NEWMAN |
| TC-FR05-AI-002 | INCOMPLETE | Từ khóa `phone` không gắn với fixture nên `≥1` không ổn định. | Lấy `name` từ baseline; 200 và mọi kết quả chứa keyword, ít nhất 1 fixture nguồn. | NEWMAN |
| TC-FR05-AI-003 | VALID | Search tên không tồn tại có empty-array oracle rõ. | Dùng sentinel duy nhất theo run; 200, array, length = 0. | NEWMAN |
| TC-FR05-AI-016 | VALID | Tautology payload là black-box SEC-05 probe phù hợp. | So baseline + sentinel literal; 200 array, không mở rộng, không SQL error. | NEWMAN |
| TC-FR05-AI-026 | VALID | Integer ID là schema assertion ổn định. | Baseline 200; từng `id` là positive integer. | NEWMAN |

## Traceability Matrix mẫu

| Case ID | Final intent | Execution class | Postman folder/request | Assertion ID | Latest result source |
| --- | --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | Baseline list 200 JSON array with required fields | NEWMAN | FR-05 - Product Search / TC-FR05-AI-001 | TC-FR05-AI-001 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-002 | Dynamic keyword found, results match | NEWMAN | FR-05 - Product Search / TC-FR05-AI-002 | TC-FR05-AI-002 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-003 | Unique sentinel returns empty array | NEWMAN | FR-05 - Product Search / TC-FR05-AI-003 | TC-FR05-AI-003 | src/newman/member-2/fr-05.json |

## Ghi chú

- Cột `Verdict` luôn để `[Manual by user]` khi skill vừa sinh xong. Human phải review và gán VALID/INVALID/INCOMPLETE.
- Case ID format: `TC-FR{XX}-AI-{NNN}` cho AI-generated, `TC-FR{XX}-HUMAN-{NNN}` cho human-designed.
- Execution class: `NEWMAN` (tự động), `BROWSER-MANUAL` (cần trình duyệt), `FAULT-INJECTION` (cần can thiệp hạ tầng), `EXCLUDED` (loại bỏ).
