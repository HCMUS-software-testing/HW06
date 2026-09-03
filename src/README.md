# HW06 - API Testing Submission (Member 2: Lê Trung Kiên - 23127075)

## 1. Thông Tin Sinh Viên & SUT (ESHop)
- **Họ và tên:** Lê Trung Kiên
- **MSSV:** 23127075
- **Vai trò trong nhóm:** Thành viên 2
- **Môi trường SUT:** Backend Express + Node.js (`http://localhost:3000`)
- **Các API phụ trách (dựa trên `eshop-sut/api_specification.md`):**
  1. **Pool A:** FR-05 - Liệt kê và tìm kiếm sản phẩm (`GET /api/products`, `GET /api/products?search=keyword`)
  2. **Pool B:** FR-08 - Thanh toán / tạo đơn hàng (`POST /api/checkout`)
  3. **Pool C:** FR-18 - Quản lý đơn hàng admin (`GET /api/admin/orders`, `PUT /api/admin/orders/:id/status`)

---

## 2. Bảng Tự Đánh Giá (Self-Assessment Table)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá |
| --- | --- | ---: | ---: |
| 1 | **API 1 (FR-05):** Toàn bộ pipeline (Generate >=35 cases, Audit VALID/INVALID/INCOMPLETE, Extend >=5 cases, Newman execution + `X-Student-Id`, Bug reports) | 30 | 26 |
| 2 | **API 2 (FR-08):** Toàn bộ pipeline (Generate >=35 cases, Audit VALID/INVALID/INCOMPLETE, Extend >=5 cases, Newman execution + `X-Student-Id`, Bug reports) | 30 | 25 |
| 3 | **API 3 (FR-18):** Toàn bộ pipeline (Generate >=35 cases, Audit VALID/INVALID/INCOMPLETE, Extend >=5 cases, Newman execution + `X-Student-Id`, Bug reports) | 30 | 26 |
| 4 | **Agent Skill:** Bộ sinh test API dẫn dắt bởi AI (Sơ đồ tự vẽ + Pseudocode + Reusable Agent Skill) | 10 | 7 |
| **Tổng** | **Tổng cộng điểm bài tập HW06** | **100** | **84** |

Điểm trên chỉ phản ánh artifact local đã có: 135 authored cases, 91 Newman mappings, `summary.json` (90 assertions; 52 ok; 38 not ok), và 12 bug records.

Các tiêu chí ngoài repo vẫn để marker riêng. Không tự cho 100.

---

## 3. Báo Cáo Tóm Tắt Kiểm Thử (Test Execution Summary)

Nguồn đếm: Markdown case files + `src/test-cases/member-2-traceability.md` + `src/newman/member-2/summary.json` (generatedAt `2026-09-03T02:43:08.840Z`). Không lấy số từ bản README cũ.

| Chỉ số | API 1 (FR-05) | API 2 (FR-08) | API 3 (FR-18) | Tổng cộng |
| --- | ---: | ---: | ---: | ---: |
| Số lượng test cases do AI sinh | 35 | 35 | 35 | 105 |
| Số lượng test cases đã audit | 35 | 35 | 35 | 105 |
| Số lượng test cases tự bổ sung | 10 | 10 | 10 | 30 |
| authored | 45 | 45 | 45 | 135 |
| automated | 32 | 24 | 35 | 91 |
| Tổng số test cases thực thi | 32 | 23 | 35 | 90 |
| Số test cases PASS | 28 | 2 | 22 | 52 |
| Số test cases FAIL | 4 | 21 | 13 | 38 |
| pending | 0 | 0 | 0 | 0 |
| requests | 132 | 262 | 398 | 792 |
| Số lượng lỗi (bugs) phát hiện | 1 | 8 | 3 | 12 |

Phân loại đếm:
- **authored:** 45 case ID / FR (35 AI + 10 human), tổng 135.
- **automated:** hàng NEWMAN trong traceability (91). FR-08 có 24 mapping nhưng Newman chỉ ghi 23 assertions vì một request pending trong runner.
- **executed / PASS / FAIL:** assertion totals từ Newman, không phải số case Markdown.
- **manual/not-runnable:** BROWSER-MANUAL + FAULT-INJECTION + EXCLUDED; không tính vào PASS/FAIL.

---

## 4. Cấu Trúc Sản Phẩm Trong `src/`

```text
src/
├── README.md
├── docs/
│   ├── main-report.md
│   ├── ai-critique.md
│   ├── cicd-report.md
│   ├── ai-prompt-sequence.md
│   ├── git-commit-log.txt
│   ├── ci-manual-evidence.md
│   └── manual-submission-checklist.md
├── postman/
│   ├── HW06_API_Testing.postman_collection.json
│   ├── HW06_Local.postman_environment.json
│   └── data/
├── newman/member-2/
├── test-cases/
│   ├── member-2-fr-05.md
│   ├── member-2-fr-08.md
│   ├── member-2-fr-18.md
│   ├── member-2-traceability.md
│   └── 23127075-hw06-test-cases.xlsx
├── bug-reports/member-2-bugs.md
├── agent-skill/
│   ├── diagram.mermaid
│   ├── pseudocode.md
│   └── skill-demo-notes.md
└── ai-audit/ai_audit_report.md
```

---

## 5. Tính năng Postman thực sự đã dùng

- Collection folders theo FR-05 / FR-08 / FR-18 và collection-level header `X-Student-Id`.
- Environment variables (`baseUrl`, token placeholders, studentId); token runtime không commit.
- Test scripts: một assertion ID / case NEWMAN, `pm.sendRequest` cho setup/postcondition và race FR-08.
- Data-driven JSON trong `src/postman/data/`.
- Newman CLI + reporters `cli`, `json`, `htmlextra` qua `npm run test:api`.

---

## 6. Bằng chứng chạy và lỗi

- Newman: `src/newman/member-2/fr-05.{json,html,txt}`, `fr-08.*`, `fr-18.*`, `summary.json`.
- Bugs: `src/bug-reports/member-2-bugs.md` (BUG-001 … BUG-012).
- Issue GitHub/screenshot: xem marker trong bug report.
