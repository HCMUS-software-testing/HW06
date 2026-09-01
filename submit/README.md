# HW06 — API Testing — MSSV 23127326

Public repository: <https://github.com/HCMUS-software-testing/HW06/tree/Bao>

## Phạm vi

| Pool | Feature | API được kiểm thử |
|---|---|---|
| A | FR-04 — Personal profile | `GET/PUT /api/users/me` |
| B | FR-10 — Order state machine | `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` |
| C | FR-19 — Admin user management | `GET /api/admin/users`, `DELETE /api/admin/users/:id` |

## Tóm tắt kết quả

| Feature | AI tạo | Sinh viên bổ sung | Đã audit | Executed | Pass | Fail |
|---|---:|---:|---:|---:|---:|---:|
| FR-04 | 40 | 5 | 45 | 45 | 28 | 17 |
| FR-10 | 45 | 5 | 50 | 50 | 46 | 4 |
| FR-19 | 40 | 5 | 45 | 45 | 24 | 21 |
| **Tổng** | **125** | **15** | **140** | **140** | **98** | **42** |

Full Newman run tạo **467 HTTP requests** (gồm setup/postcondition), **839 assertions**, 63 assertion fail và **0 fixture/request error**. 42 catalogue case fail được quy về **10 root defects**. Data-driven phone run có 6 partition, 12 requests, 18 assertions; bốn invalid partition làm lộ `BUG-FR04-03`.

## Tài liệu chính

- Test catalogue: `test-cases/member-4.csv`, `test-cases/member-4.json`; file XLSX cần export lại từ CSV sau thay đổi cuối.
- Postman: full collection, environment, data-driven collection + CSV và deterministic CI-demo collection trong `postman/`.
- Newman: `newman/member-4/newman-full-report.html` và `newman-report.html`.
- Bug register: `bug-reports/member-4.md`; 10 GitHub Issues công khai.
- Main report, AI Audit, AI Critique, CI/CD report: `docs/`.
- Agent Skill: pseudocode và design notes trong `agent-skill/`.

## Tính năng Postman đã dùng

Collection/folder, environment variables, collection variables, collection-level pre-request script, dynamic `pm.sendRequest` fixtures/postconditions, test scripts, exact status assertions, JSON/schema assertions, data-driven iteration CSV, Newman CLI, JSON/HTML Extra reporter và GitHub Actions artifact upload. Monitor/mock server không dùng vì SUT local và các ca cần reset SQLite cô lập.

## Tự đánh giá

| STT | Tiêu chí | Điểm | Tự đánh giá |
|---:|---|---:|---:|
| 1 | API 1 — full pipeline FR-04 | 30 | 29 |
| 2 | API 2 — full pipeline FR-10 | 30 | 29 |
| 3 | API 3 — full pipeline FR-19 | 30 | 29 |
| 4 | Agent Skill | 10 | 8 |
|  | **Tổng** | **100** | **95** |

Hai điểm Agent Skill chưa tự chấm vì sơ đồ bắt buộc phải do sinh viên tự vẽ và video là tùy chọn.

## Việc sinh viên hoàn tất thủ công trước khi ZIP

1. Mở từng GitHub Issue trong `evidence/README.md`, chụp trang Issue thật và lưu đúng tên file đã liệt kê.
2. Chụp GitHub Actions pass/fail, Postman Console có `X-Student-Id: 23127326`, và Newman HTML có `localhost`.
3. Tự vẽ lại sơ đồ Agent Skill theo `agent-skill/skill-design.md`; không nộp diagram do AI tạo.
4. Export lại XLSX/PDF từ CSV/Markdown cuối cùng; thêm video URL nếu quay video.
5. Đóng gói theo tên `23127326_HW06_AI_API_095.zip`.
