# HW06 API Testing Report — Member 4 (23127326)

## 1. Scope and oracle

SUT là EShop backend chạy tại `http://localhost:3000`, pin ở upstream commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`. Ba feature được chọn đúng ba pool là FR-04, FR-10 và FR-19. Oracle lấy từ `api_specification.md` và SRS/README của SUT; implementation chỉ dùng để điều tra sau khi test đã quan sát sai lệch.

Quy ước status: 2xx cho thao tác hợp lệ; 400 cho input/business transition không hợp lệ; 401 cho thiếu/sai xác thực; 403 cho đã xác thực nhưng sai quyền; 404 cho resource không tồn tại. Mỗi case có exact status, schema/invariant và postcondition rõ ràng.

## 2. AI-first generation, audit and extension

AI được điều khiển theo năm prompt tách biệt: trích contract; FR-04 domain/security/schema; FR-10 state graph; FR-19 authorization/delete; audit/deduplicate/extension. AI tạo 125 case (40/45/40). Sinh viên audit từng dòng, sửa oracle/fixture/mapping và bổ sung 15 case HUMAN (5 mỗi feature). Catalogue cuối cùng có 140/140 nhãn `VALID`; các cột `Audit reason`, `Corrected version`, `Why AI missed` giữ vết quyết định.

Chi tiết audit và mapping Postman nằm trong `../test-cases/member-4.csv` và JSON tương đương.

## 3. Coverage theo feature

### FR-04 — Personal profile (45 cases)

`GET /api/users/me` kiểm tra token, identity binding, exact object schema, sensitive fields và tính lặp lại. `PUT /api/users/me` bao phủ phone 10/11 chữ số bắt đầu bằng 0, name/address boundary, null/type, empty/partial body, email/role mass assignment, XSS text và cross-user isolation.

### FR-10 — Order state machine (50 cases)

Suite bao phủ ma trận 5×5 giữa `pending`, `confirmed`, `shipping`, `delivered`, `canceled`; valid path `pending → confirmed → shipping → delivered`; cancellation từ pending/confirmed; terminal state, backward/skip/replay transition, ownership, admin role, malformed status/ID và response schema. Mỗi case tạo order riêng và GET lại để kiểm tra state.

### FR-19 — Admin user management (45 cases)

`GET /api/admin/users` kiểm tra admin-only, token, list schema và absence of credential fields. `DELETE /api/admin/users/:id` kiểm tra valid/missing/malformed ID, repeated/concurrent delete, SQL-injection payload, IDOR/regular user, stale JWT, self-delete và postcondition user list. Self-delete chạy cuối suite.

### Security mapping

SEC-01 được quan sát qua việc API làm lộ plaintext password; SEC-02 qua token missing/invalid/stale; SEC-03 qua admin role; SEC-04 qua XSS payload được lưu/round-trip dưới dạng data (UI escaping nằm ngoài phạm vi API); SEC-05 qua injection payload và state invariants; SEC-06 qua protected `role`. SEC-07 chỉ áp dụng OTP reset-password FR-03 nên được ghi `N/A` cho ba API đã chọn, không bịa test OTP ngoài phạm vi.

## 4. Postman implementation

Full collection gồm hai setup login và 140 catalogue item. Collection-level pre-request script bắt buộc `studentId`, upsert header `X-Student-Id` và log request. Fixture cô lập, cleanup và postcondition được thực hiện bằng `pm.sendRequest`. Assertions kiểm tra exact status, JSON content type, body shape, identity/state và không có 5xx không xử lý.

Tính năng đã dùng: collection/folder, environment/collection/local variables, pre-request/test scripts, dynamic fixtures, data-driven CSV, Collection Runner-compatible data, Newman CLI, JSON/HTML Extra reports và CI artifact. Monitor/mock server không phù hợp vì suite cần reset local SQLite và chạy fixture phá hủy có kiểm soát.

## 5. Execution result

Full run ngày 2026-09-01 trên clean database:

| Metric | Result |
|---|---:|
| Catalogue cases | 140 |
| Catalogue PASS / FAIL | 98 / 42 |
| HTTP requests, including setup/postconditions | 467 |
| Assertions | 839 |
| Failed assertions | 63 |
| Fixture/request errors | 0 |
| Root defects | 10 |

Data-driven FR-04 phone run: 6 iterations, 12 requests, 18 assertions, 4 fail. Hai valid partition pass; bốn invalid partition bị SUT chấp nhận sai. Báo cáo: `../newman/member-4/newman-full-report.html`, `newman-report.html`; phân loại chi tiết: `failure-classification.md`.

## 6. Defect analysis

42 case fail quy về 10 root defects: mass assignment role, credential exposure, missing phone validation, unsafe partial/body update, hai sai state rule FR-10, missing admin-role enforcement, delete-user success sai semantics, stale JWT và self-delete. Không đếm mỗi assertion fail thành một bug. Reproduction, expected/actual, severity, test IDs và public GitHub Issue nằm trong `../bug-reports/member-4.md`.

## 7. CI/CD

Workflow `.github/workflows/hw06-member4.yml` clone/pin SUT, khởi động database sạch, validate secret MSSV, chạy Newman và upload report. CI-demo có ba stable case đại diện FR-04/FR-10/FR-19 cùng một controlled assertion: `false` cho 22/22 pass; `true` tạo đúng 1 assertion fail. Chế độ `workflow_dispatch: conformance` chạy toàn bộ 140 case và giữ các product defect hiển thị màu đỏ. CI-demo failure được ghi rõ là pipeline-control evidence, không phải bug sản phẩm.

## 8. Agent Skill design

Thiết kế reusable generator có contract normalizer, bốn planner domain/state/security/schema, candidate critic/deduplicator, human approval gate, exporter và execution feedback loop. Pseudocode trong `../agent-skill/pseudocode.md`. Theo ràng buộc chống gian lận, sơ đồ nộp cuối phải do sinh viên tự vẽ; AI chỉ cung cấp checklist nút/cạnh trong `skill-design.md`.

## 9. AI Audit appendix

Toàn bộ khai báo công cụ, thời gian, prompt, output và human decision được đính kèm trong `ai-audit-report.md`. Row-level AI output được giữ nguyên trong JSON test catalogue; 15 row HUMAN không bị trộn vào output AI.

## 10. Evidence integrity and manual handoff

Không dùng console/Issue card dựng. Ảnh GitHub Issues và Actions phải chụp trực tiếp trang thật; Postman Console và Newman hostname phải chụp từ run thật. Danh sách tên file/URL cần chụp nằm trong `../evidence/README.md`. Sinh viên export PDF/XLSX, tự vẽ diagram, quay video tùy chọn và đóng ZIP sau cùng.
