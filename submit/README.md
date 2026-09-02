# HW06 — API Testing — MSSV 23127326

Public repository: <https://github.com/HCMUS-software-testing/HW06/tree/Bao>

Phạm vi đếm: mỗi feature được xem là một API nghiệp vụ gồm các endpoint công khai của feature đó; mục tiêu `>=35` được áp dụng cho từng nhóm FR-04, FR-10 và FR-19. Catalogue vẫn ghi rõ từng method/endpoint và mapping Postman riêng.

## Phạm vi

| Pool | Feature                       | API được kiểm thử                                                |
| ---- | ----------------------------- | ---------------------------------------------------------------- |
| A    | FR-04 — Personal profile      | `GET/PUT /api/users/me`                                          |
| B    | FR-10 — Order state machine   | `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` |
| C    | FR-19 — Admin user management | `GET /api/admin/users`, `DELETE /api/admin/users/:id`            |

## Tóm tắt kết quả

| Feature  |  AI tạo | Sinh viên bổ sung | Đã audit | Executed |   Pass |   Fail |
| -------- | ------: | ----------------: | -------: | -------: | -----: | -----: |
| FR-04    |      40 |                 5 |       45 |       45 |     30 |     15 |
| FR-10    |      45 |                 5 |       50 |       50 |     46 |      4 |
| FR-19    |      40 |                 5 |       45 |       45 |     22 |     23 |
| **Tổng** | **125** |            **15** |  **140** |  **140** | **98** | **42** |

Full Newman run tạo **467 HTTP requests** (gồm setup/postcondition), **839 assertions**, 63 assertion fail và **0 fixture/request error**. 42 catalogue case fail được quy về **10 root defects**. Data-driven phone run có 6 partition, 12 requests, 18 assertions; bốn invalid partition làm lộ `BUG-FR04-03`.

CI full-pass gate chạy lại chính collection 140 case trên corrected SUT baseline: 467 requests, 839 assertions, 0 assertion fail. `ci-demo` chỉ là minh chứng điều khiển pipeline 22 assertions; `conformance` trên SUT upstream nguyên bản vẫn ghi nhận 42 case fail.

## Tài liệu chính

- Test catalogue: `test-cases/23127326.csv`, `test-cases/23127326.json`; file XLSX đã được đồng bộ với catalogue cuối và có summary tính bằng công thức.
- AI traceability: `AI-001` chuẩn hóa contract; `AI-002` sinh FR-04 (40 case), `AI-003` sinh FR-10 (45 case), `AI-004` sinh FR-19 (40 case); 15 case mở rộng có nguồn `HUMAN-001`.
- Postman: full collection, environment, data-driven collection + CSV và deterministic CI-demo collection trong `postman/`.
- Newman: `newman-full-report.html`, `newman-report.html` và full-pass CI evidence `ci-full-pass-report.html`/`.json`.
- Bug register: `bug-reports.md`; 10 GitHub Issues công khai.
- Main report, AI Audit, AI Critique, CI/CD report và failure classification nằm trực tiếp trong `submit/`.
- Agent Skill: `agent-skill/api-test-generator/SKILL.md`, schema, pseudocode và design notes trong `agent-skill/`.
- Video demo Agent Skill: [DemoAgentSkill-HW06](https://youtu.be/1X8fNBIZYV0).

## Tính năng Postman đã dùng

Collection/folder, environment variables, collection variables, collection-level pre-request script, dynamic `pm.sendRequest` fixtures/postconditions, test scripts, exact status assertions, JSON/schema assertions, data-driven iteration CSV, Newman CLI, JSON/HTML Extra reporter và GitHub Actions artifact upload. Monitor/mock server không dùng vì SUT local và các ca cần reset SQLite cô lập.

Ghi chú minh chứng lịch sử: `newman-full-localhost.png` và các ảnh GitHub Actions được chụp từ các run công khai trước khi đổi tên workflow/collection từ “Member 4” sang MSSV `23127326`. Nội dung ảnh được giữ nguyên để bảo toàn bằng chứng gốc; tên hiện tại được thể hiện trong `newman-full-report.html`, collection và workflow mới.

## Tự đánh giá

|  STT | Tiêu chí                    |    Điểm | Tự đánh giá |
| ---: | --------------------------- | ------: | ----------: |
|    1 | API 1 — full pipeline FR-04 |      30 |          30 |
|    2 | API 2 — full pipeline FR-10 |      30 |          30 |
|    3 | API 3 — full pipeline FR-19 |      30 |          30 |
|    4 | Agent Skill                 |      10 |          10 |
|      | **Tổng**                    | **100** |     **100** |

Điểm Agent Skill được tự chấm đủ 10/10 nhờ có skill reusable, schema, pseudocode, sơ đồ tự thiết kế/tự vẽ và video demo.

## Checklist bàn giao

| Hạng mục bắt buộc                                         | Trạng thái / vị trí                                         |
| --------------------------------------------------------- | ----------------------------------------------------------- |
| Báo cáo chính gồm kiểm thử API + phụ lục AI Audit         | `main-report.md`, `main-report.pdf`                         |
| Public GitHub repository                                  | Link ở đầu file này                                         |
| Postman collections, environment và Newman HTML/JSON      | `postman/`, `newman-full-report.html`, `newman-report.html` |
| Danh sách tính năng Postman                               | Mục “Tính năng Postman đã dùng” bên dưới                    |
| CI/CD report, full-suite pass, run đúng một failure, ảnh và link | `cicd-report.md`, `evidence/`, `ci/`                 |
| Workflow CI/CD                                             | `.github/workflows/hw06-23127326.yml`                       |
| Excel test cases + test summary                           | `23127326_test-cases.xlsx` gồm 2 sheet                      |
| Agent Skill, sơ đồ và pseudocode                          | `agent-skill/`                                              |
| Bug report + GitHub Issue screenshots                     | `bug-reports.md`, `evidence/`                               |
| AI Audit và AI Critique Markdown + PDF                    | `ai-audit-report.*`, `ai-critique.*`                        |
| Git commit log                                            | `git_commit_log.txt`                                        |

Video demo Agent Skill: [https://youtu.be/1X8fNBIZYV0](https://youtu.be/1X8fNBIZYV0).
