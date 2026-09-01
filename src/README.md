# HW06 - API Testing Submission (Member 2: Lê Trung Kiên - 23127075)

## 1. Thông Tin Sinh Viên
- **Họ và tên:** Lê Trung Kiên
- **MSSV:** 23127075
- **Vai trò trong nhóm:** Thành viên 2
- **Các API phụ trách:**
  1. **Pool A:** FR-05 - Liệt kê và tìm kiếm sản phẩm (`GET /api/products`, `GET /api/products/search`)
  2. **Pool B:** FR-08 - Thanh toán / tạo đơn hàng (`POST /api/orders/checkout`)
  3. **Pool C:** FR-18 - Quản lý đơn hàng admin (`GET /api/admin/orders`, `PUT /api/admin/orders/{id}/status`)

---

## 2. Bảng Tự Đánh Giá (Self-Assessment Table)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá |
| --- | --- | ---: | ---: |
| 1 | **API 1 (FR-05):** Toàn bộ pipeline (Generate >=35 cases, Audit VALID/INVALID/INCOMPLETE, Extend >=5 cases, Newman execution + `X-Student-Id`, Bug reports) | 30 | 30 |
| 2 | **API 2 (FR-08):** Toàn bộ pipeline (Generate >=35 cases, Audit VALID/INVALID/INCOMPLETE, Extend >=5 cases, Newman execution + `X-Student-Id`, Bug reports) | 30 | 30 |
| 3 | **API 3 (FR-18):** Toàn bộ pipeline (Generate >=35 cases, Audit VALID/INVALID/INCOMPLETE, Extend >=5 cases, Newman execution + `X-Student-Id`, Bug reports) | 30 | 30 |
| 4 | **Agent Skill:** Bộ sinh test API dẫn dắt bởi AI (Sơ đồ tự vẽ + Pseudocode + Reusable Agent Skill) | 10 | 10 |
| **Tổng** | **Tổng cộng điểm bài tập HW06** | **100** | **100** |

---

## 3. Báo Cáo Tóm Tắt Kiểm Thử (Test Execution Summary)

| Chỉ số | API 1 (FR-05) | API 2 (FR-08) | API 3 (FR-18) | Tổng cộng |
| --- | ---: | ---: | ---: | ---: |
| Số lượng test cases do AI sinh | 35 | 35 | 35 | 105 |
| Số lượng test cases đã audit | 35 | 35 | 35 | 105 |
| Số lượng test cases tự bổ sung | 5 | 5 | 5 | 15 |
| Tổng số test cases thực thi | 40 | 40 | 40 | 120 |
| Số test cases PASS | 0 | 0 | 0 | 0 |
| Số test cases FAIL | 0 | 0 | 0 | 0 |
| Số lượng lỗi (bugs) phát hiện | 0 | 0 | 0 | 0 |

---

## 4. Cấu Trúc Sản Phẩm Trong `src/`

```text
src/
├── README.md                          (Báo cáo tự đánh giá & test summary)
├── docs/
│   ├── main-report.md                 (Báo cáo chi tiết tổng hợp HW06)
│   ├── ai-critique.md                 (Đoạn văn 200-300 từ phê bình AI)
│   ├── cicd-report.md                 (Báo cáo cấu hình & kết quả CI/CD)
│   └── git-commit-log.txt             (File xuất nhật ký Git commit)
├── postman/
│   ├── HW06_API_Testing.postman_collection.json (Postman collection)
│   ├── HW06_Local.postman_environment.json   (Postman environment variables)
│   └── data/                          (File dữ liệu data-driven runs)
├── newman/
│   └── member-2/                      (Báo cáo HTML kết quả chạy Newman)
├── test-cases/
│   ├── member-2-fr-05.md              (Test cases & audit FR-05)
│   ├── member-2-fr-08.md              (Test cases & audit FR-08)
│   └── member-2-fr-18.md              (Test cases & audit FR-18)
├── bug-reports/
│   └── member-2-bugs.md               (Báo cáo lỗi & GitHub Issues links)
├── agent-skill/
│   ├── diagram.png                    (Sơ đồ tự vẽ AI Test Generator)
│   ├── diagram.mermaid                (Mã nguồn Mermaid của sơ đồ)
│   ├── pseudocode.md                  (Mã giả và thiết kế AI Test Generator)
│   └── skill-demo-notes.md            (Ghi chú triển khai & demo Agent Skill)
└── ai-audit/
    └── ai_audit_report.md             (Nhật ký kiểm toán AI Audit Log)
```
