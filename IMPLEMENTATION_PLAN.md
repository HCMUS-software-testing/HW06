# Kế Hoạch Thực Hiện Bài Tập HW06 - API Testing (Đạt 100/100 Điểm)

> **Sinh viên thực hiện:** Lê Trung Kiên (MSSV: 23127075) - Thành viên 2  
> **Các API phụ trách:**  
> 1. **FR-05 (Pool A):** Liệt kê và tìm kiếm sản phẩm (`GET /api/products`, `GET /api/products/search`)  
> 2. **FR-08 (Pool B):** Thanh toán / tạo đơn hàng (`POST /api/orders/checkout`)  
> 3. **FR-18 (Pool C):** Quản lý đơn hàng Admin (`GET /api/admin/orders`, `PUT /api/admin/orders/{id}/status`)  

---

## 1. Mục Tiêu Và Cấu Trúc Điểm (100/100 Points)

| Hạng mục | Chi tiết công việc | Điểm |
| --- | --- | ---: |
| **API 1 (FR-05)** | Generate >=35 AI cases, Audit, Extend >=5 Human cases, Newman HTML report, `X-Student-Id: 23127075` header, Bug reports | 30 |
| **API 2 (FR-08)** | Generate >=35 AI cases, Audit, Extend >=5 Human cases, Newman HTML report, `X-Student-Id: 23127075` header, Bug reports | 30 |
| **API 3 (FR-18)** | Generate >=35 AI cases, Audit, Extend >=5 Human cases, Newman HTML report, `X-Student-Id: 23127075` header, Bug reports | 30 |
| **Agent Skill** | Bộ sinh test API dẫn dắt bởi AI: Sơ đồ tự vẽ + Pseudocode + Reusable Agent Skill notes | 10 |
| **Tổng cộng** | **Tự đánh giá đạt tối đa 100/100 điểm** | **100** |

---

## 2. Cấu Trúc Khung Bài Nộp Trong `src/`

Tất cả các sản phẩm bài làm nằm trực tiếp trong `src/` (thư mục làm bài chính):

```text
src/
├── README.md                          (Báo cáo tự đánh giá 100/100 & bảng tóm tắt test)
├── docs/
│   ├── main-report.md                 (Báo cáo tổng hợp bài tập HW06)
│   ├── ai-critique.md                 (Đoạn văn 200-300 từ phê bình AI)
│   ├── cicd-report.md                 (Báo cáo cấu hình & chạy CI/CD Newman)
│   └── git-commit-log.txt             (File văn bản xuất nhật ký Git commit)
├── postman/
│   ├── HW06_API_Testing.postman_collection.json (Postman collection + header pre-request)
│   ├── HW06_Local.postman_environment.json   (Postman environment variables)
│   └── data/                          (File dữ liệu data-driven runs)
├── newman/
│   └── member-2/                      (Báo cáo HTML Newman execution)
├── test-cases/
│   ├── member-2-fr-05.md              (Bảng test cases AI & audit FR-05)
│   ├── member-2-fr-08.md              (Bảng test cases AI & audit FR-08)
│   └── member-2-fr-18.md              (Bảng test cases AI & audit FR-18)
├── bug-reports/
│   └── member-2-bugs.md               (Báo cáo bug & link GitHub Issues kèm screenshots)
├── agent-skill/
│   ├── diagram.png                    (Sơ đồ tự vẽ AI Test Generator)
│   ├── diagram.mermaid                (Mã nguồn Mermaid sơ đồ)
│   ├── pseudocode.md                  (Mã giả & thiết kế chi tiết)
│   └── skill-demo-notes.md            (Ghi chú minh họa & YouTube link demo)
└── ai-audit/
    └── ai_audit_report.md             (Nhật ký Báo cáo Kiểm toán AI)
```

---

## 3. Danh Sách Các Task Thực Hiện Từng Bước

### Task 1: Thiết Lập Hạ Tầng Postman & Pre-request Script
- **Nội dung:** Cấu hình file `HW06_Local.postman_environment.json` (`baseUrl`, `studentId=23127075`, `userToken`, `adminToken`).
- **Pre-request Script:** Thêm script tự động chèn header `X-Student-Id: 23127075` vào mọi request trong Collection `HW06_API_Testing.postman_collection.json`.
- **Commit:** `test(member-2): setup Postman collection and environment infrastructure`

### Task 2: Pipeline API 1 - FR-05 (Liệt Kê & Tìm Kiếm Sản Phẩm)
- **Endpoint:** `GET /api/products`, `GET /api/products/search`
- **Bước 1 (AI Generation):** Sinh >= 35 test cases (Domain partitioning, query parameters, sorting, pagination, security SQLi, response schema).
- **Bước 2 (Audit):** Kiểm toán từng case với nhãn `VALID`, `INVALID`, hoặc `INCOMPLETE` kèm lý do & hướng sửa.
- **Bước 3 (Extension):** Thiết kế tự thêm >= 5 test cases human-written (bảo mật injection, boundary values) & giải thích lý do AI bỏ sót.
- **Bước 4 (Execution):** Implement trong Postman collection và chạy Newman xuất file report `src/newman/member-2/FR05_Report.html`.
- **Commit:** `test(member-2): complete FR-05 test generation, audit, extension, and execution`

### Task 3: Pipeline API 2 - FR-08 (Thanh Toán / Tạo Đơn Hàng)
- **Endpoint:** `POST /api/orders/checkout`
- **Bước 1 (AI Generation):** Sinh >= 35 test cases (Valid checkout, empty cart, stock limits, coupon interactions, unauthenticated, schema validation).
- **Bước 2 (Audit):** Gán nhãn `VALID` / `INVALID` / `INCOMPLETE` kèm lý do sửa.
- **Bước 3 (Extension):** Thêm >= 5 test cases human-written (race condition, negative quantity/stock, multi-session cart manipulation).
- **Bước 4 (Execution):** Chạy Newman xuất report `src/newman/member-2/FR08_Report.html`.
- **Commit:** `test(member-2): complete FR-08 test generation, audit, extension, and execution`

### Task 4: Pipeline API 3 - FR-18 (Quản Lý Đơn Hàng Admin)
- **Endpoint:** `GET /api/admin/orders`, `PUT /api/admin/orders/{id}/status`
- **Bước 1 (AI Generation):** Sinh >= 35 test cases (Admin auth, order listing, status machine transitions Pending->Confirmed->Shipping->Delivered, invalid state transitions, schema).
- **Bước 2 (Audit):** Kiểm toán toàn bộ test cases.
- **Bước 3 (Extension):** Thêm >= 5 test cases human-written (Privilege Escalation, IDOR trên order status update, rollback trạng thái không hợp lệ).
- **Bước 4 (Execution):** Chạy Newman xuất report `src/newman/member-2/FR18_Report.html`.
- **Commit:** `test(member-2): complete FR-18 test generation, audit, extension, and execution`

### Task 5: Agent Skill - AI Test Generator Design
- **Mục tiêu:** Đạt 10/10 điểm phần Agent Skill.
- **Bước 1:** Vẽ sơ đồ luồng dữ liệu tự động sinh test tại `src/agent-skill/diagram.mermaid` & `diagram.png`.
- **Bước 2:** Viết pseudocode chi tiết pipeline 4 giai đoạn sinh thử nghiệm tại `src/agent-skill/pseudocode.md`.
- **Bước 3:** Hoàn thiện ghi chú hướng dẫn và demo link tại `src/agent-skill/skill-demo-notes.md`.
- **Commit:** `feat(member-2): design AI Test Generator Agent Skill with diagram and pseudocode`

### Task 6: Tích Hợp CI/CD, Bug Reports, AI Critique & Báo Cáo Cuối
- **Bug Reports:** Báo cáo các lỗi thật phát hiện vào `src/bug-reports/member-2-bugs.md` và tạo GitHub Issues kèm ảnh chụp màn hình.
- **CI/CD Report:** Cấu hình GitHub Actions chạy Newman; chụp ảnh và lưu minh chứng 1 run PASS toàn bộ và 1 run FAIL có chủ đích tại `src/docs/cicd-report.md`.
- **AI Critique:** Viết đoạn văn 200-300 từ phân tích lỗi, thiên lệch của AI tại `src/docs/ai-critique.md`.
- **Đóng gói & Commit Log:** Xuất `git log` ra `src/docs/git-commit-log.txt`. Hoàn thiện `src/README.md` tự đánh giá 100/100 điểm.
- **Commit:** `docs(member-2): complete HW06 main report, AI critique, CI/CD report, and self-assessment`
