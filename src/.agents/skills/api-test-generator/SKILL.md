---
name: api-test-generator
description: "Use when generating API test cases from an API specification (OpenAPI/Markdown) for the EShop SUT or similar backend APIs. Implements a structured 6-step pipeline: parse contracts, generate domain/state/security/schema cases, deduplicate, and export for human review."
---

# AI-Driven API Test Generator

Skill tự động sinh candidate test cases API từ đặc tả, rồi **dừng** cho người review.
Case chỉ thành final/executable sau nhãn người `VALID`, `INVALID`, hoặc `INCOMPLETE` và quyết định correction/exclusion.

## Khi nào sử dụng

- User yêu cầu sinh test cases API cho một endpoint hoặc functional requirement.
- User cung cấp API spec (Markdown, OpenAPI YAML/JSON) hoặc trỏ tới file spec trong repo.
- User muốn mở rộng bộ test đã có với thêm case mới.

## Đầu vào bắt buộc

1. **API Specification:** File hoặc đường dẫn tới `api_specification.md`, OpenAPI YAML/JSON, hoặc mô tả endpoint.
2. **Target Functional Requirement:** Ví dụ FR-05, FR-08, FR-18.
3. **Security Requirements:** SEC-01..SEC-07 (nếu có trong spec).

## Pipeline 6 bước

### Bước 1: Parse Contracts

Đọc API spec và trích xuất:
- **Endpoint map:** method, route, parameters, request body schema.
- **Response schemas:** success (2xx) và error (4xx/5xx) response shapes.
- **RBAC rules:** roles required per endpoint (admin, user, public).
- **State machine:** order lifecycle (pending → confirmed → shipping → delivered, cancel rules).

```
Kết quả: ContractBundle(endpoints, requirements, security_rules, state_models)
```

### Bước 2: Domain Partitioning

Cho mỗi parameter của endpoint, sinh test cases bao phủ:
- **Valid:** Giá trị hợp lệ tiêu biểu.
- **Invalid:** Giá trị không hợp lệ (type sai, null, rỗng, quá dài).
- **Boundary:** Biên của miền (0, -1, max_int, empty string, 255+ chars).

Mỗi case phải có:
- Case ID theo format `TC-FR{XX}-AI-{NNN}` (NNN bắt đầu từ 001).
- Method, endpoint, params/body cụ thể.
- Expected status code.
- Expected response body/schema assertion.

### Bước 3: State Machine Paths

Nếu endpoint liên quan tới state transitions (ví dụ FR-10 order state machine):
- **Happy paths:** pending → confirmed → shipping → delivered.
- **Illegal transitions:** delivered → pending, canceled → shipping, canceled → delivered.
- **Terminal states:** Xác nhận delivered và canceled là terminal, không chuyển tiếp được.

### Bước 4: Security Cases (SEC-01..SEC-07)

Sinh test cases cho:
- **Missing token:** Request không có Authorization header → 401.
- **Invalid token:** Token hết hạn hoặc giả → 401/403.
- **Wrong role:** User token gọi admin endpoint → 403.
- **IDOR:** Cross-user resource access.
- **SQL Injection:** Tautology, UNION, comment, stacked queries trên search/params.
- **XSS:** Script tags, event handlers trong input (API-level: không reflect trong JSON).
- **Mass assignment:** Client gửi `role: "admin"` trong profile update → bị ignore.

### Bước 5: Schema Validation

Sinh test cases kiểm tra response shape:
- Mỗi field required phải có mặt với đúng type.
- `Content-Type: application/json` cho mọi response.
- Không rò rỉ fields nhạy cảm (password, token, secret).

### Bước 6: Deduplicate & Human Review Gate

```
HARD GATE: Không case nào được coi là final hoặc executable trước khi human review.
```

1. **Semantic dedup:** Loại case trùng theo (method, route, auth_mode, payload_canonical, oracle).
2. **Gắn Audit Verdict placeholder:** Mỗi case có cột `Verdict` để trống `[Manual by user]`.
3. **Export:** Xuất bảng Markdown + traceability matrix.

## Output Format

Xuất test cases dưới dạng bảng Markdown:

```markdown
| STT | Case ID | Description | Method | Endpoint | Params/Body | Expected Status | Expected Body | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC-FR05-AI-001 | Baseline list returns 200 JSON array | GET | /api/products | (none) | 200 | JSON array with id, name, price, ... | [Manual by user] |
```

Sau đó xuất bảng audit:

```markdown
| ID | Verdict | Technical reason | Final correction | Execution class |
| --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | [Manual by user] | [Manual by user] | [Manual by user] | NEWMAN / EXCLUDED / BROWSER-MANUAL |
```

## Ràng buộc

- **Mục tiêu:** ≥ 35 AI cases per FR.
- Generator **không** tự gán VALID/INVALID — chỉ sinh candidate.
- INVALID duplicate phải EXCLUDED, không chạy NEWMAN lần hai.
- Execution ingestion chỉ đếm assertion Newman; README/Excel phải lấy số từ `summary.json`.
- Mỗi case NEWMAN phải có assertion ID trùng case ID (1-1 mapping).
- Không bịa kết quả CI/CD, screenshot, hay GitHub issue.

## Tham khảo thiết kế

- Sơ đồ luồng: `resources/diagram.mermaid` (sơ đồ do sinh viên tự vẽ — không regenerate).
- Pseudocode chi tiết: `resources/pseudocode.md`.
- Ví dụ output: `examples/fr-05-sample-output.md`.

## Sau khi sinh xong

1. Thông báo cho user tổng số case đã sinh, phân bố theo category.
2. Nhắc user cần audit từng case (VALID/INVALID/INCOMPLETE).
3. Hỏi user có muốn sinh thêm human-designed cases bổ sung không.
4. Nếu user yêu cầu, hỗ trợ export sang Postman Collection format.
