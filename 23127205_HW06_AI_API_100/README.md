# HW06 - Kiểm Thử API & Ứng Dụng AI (Software Testing)

## 1. Thông Tin Sinh Viên
- **Họ và tên:** Lâm Hữu Khánh
- **Mã số sinh viên:** `23127205`
- **Vai trò trong nhóm:** Thành viên 1
- **Bộ ba API phụ trách:**
  - **Pool A:** FR-02: Đăng nhập & Khóa tài khoản (`POST /api/login`)
  - **Pool B:** FR-07: Giỏ hàng (`GET /api/cart`, `POST /api/cart`)
  - **Pool C:** FR-15: Quản lý sản phẩm CRUD (`POST/GET/PUT/DELETE /api/products`)
- **Repository GitHub:** https://github.com/HCMUS-software-testing/HW06.git
- **Branch nộp bài:** `khanh`

---

## 2. Bảng Tự Đánh Giá Điểm (Self-Assessment Rubric)

| STT | Tiêu chí đánh giá theo Đề bài HW06 | Điểm tối đa | Điểm tự đánh giá | Minh chứng & Báo cáo Deliverables |
|:---:|---|:---:|:---:|---|
| 1 | **API 1 (FR-02: Login & Lockout)** — Pipeline toàn bộ (Generate + Audit + Extend + Execute + 4 Bugs) | 30 | 30 | `postman/`, `newman/member-1/fr02-report.html`, `test-cases/member-1.xlsx`, `reports/main-report.md` |
| 2 | **API 2 (FR-07: Shopping Cart)** — Pipeline toàn bộ (Generate + Audit + Extend + Execute + 4 Bugs) | 30 | 30 | `postman/`, `newman/member-1/fr07-report.html`, `test-cases/member-1.xlsx`, `reports/main-report.md` |
| 3 | **API 3 (FR-15: Product CRUD)** — Pipeline toàn bộ (Generate + Audit + Extend + Execute + 4 Bugs) | 30 | 30 | `postman/`, `newman/member-1/fr15-report.html`, `test-cases/member-1.xlsx`, `reports/main-report.md` |
| 4 | **Agent Skill (G9.5 - Create)** — Bộ sinh test API tự động từ đặc tả OpenAPI | 10 | 10 | `agent-skill/diagram.png`, `agent-skill/pseudocode.md`, `agent-skill/skill.py`, `agent-skill/SKILL.md` |
| | **TỔNG ĐIỂM BÀI TẬP** | **100** | **100** | **Gói nộp bài: `23127205_HW06_AI_API_100.zip`** |

---

## 3. Báo Cáo Tóm Tắt Kiểm Thử (Test Execution Summary)

| Chỉ số tổng hợp | FR-02 (Login & Lockout) | FR-07 (Cart) | FR-15 (Product CRUD) | TỔNG CỘNG |
|---|:---:|:---:|:---:|:---:|
| **Test Cases AI Sinh ra** | 38 | 38 | 38 | **114** |
| **Test Cases được Audit** | 38 | 38 | 38 | **114 (100%)** |
| **Test Cases Con người Tự thêm** | 6 | 6 | 6 | **18** |
| **Tổng số Test Cases Thiết kế** | **44** | **44** | **44** | **132** |
| **Requests thực thi trong Sanity Suite** | 18 | 12 | 11 | **41 (+2 Auth = 43)** |
| **Assertions Pass trên Sanity Suite (CI)** | 48 | 34 | 36 | **118 (100% Green)** |
| **Requests Bắt Bug (Bug Discovery Suite)** | 2 | 4 | 3 | **9 Requests** |
| **Số lỗi thật (Bugs) phát hiện & Báo cáo** | **4** | **4** | **4** | **12 Bugs (Log Issues #1-#12)** |

---

## 4. Cấu Trúc Thư Mục Bàn Giao Chuẩn Quy Cách

```text
23127205_HW06_AI_API_100/
├── README.md                           # Bảng tự đánh giá và báo cáo tóm tắt chỉ số kiểm thử
├── reports/                            # Thư mục chứa TOÀN BỘ BÁO CÁO & MINH CHỨNG
│   ├── main-report.md & .pdf           # Báo cáo tổng hợp chính bài tập HW06
│   ├── cicd-report.md & .pdf           # Báo cáo cấu hình CI/CD & 2 commit runs mẫu (Pass/Fail)
│   ├── ai-audit-report.md & .pdf       # Báo cáo kiểm toán AI toàn bộ phiên làm việc
│   ├── ai-critique.md & .pdf           # Đoạn văn 200-300 từ phê bình AI
│   ├── bug-report.md                   # Báo cáo chi tiết 12 Lỗi & Lỗ hổng bảo mật SUT
│   ├── git-commit-log.txt              # Nhật ký commit Git text log
│   └── screenshots/                    # Ảnh chụp minh chứng console, local run, CI/CD, GitHub Issues
├── docs/                               # Thư mục TÀI LIỆU THAM KHẢO & ĐẶC TẢ
│   ├── req/                            # Yêu cầu đề bài HW06 (Tiếng Việt & Tiếng Anh MD/PDF)
│   ├── implementation_plan.md          # Kế hoạch triển khai kỹ thuật kiểm thử chi tiết
│   ├── openapi.yaml                    # Đặc tả OpenAPI 3.0 YAML chuẩn hóa của SUT
│   ├── istqb-ct-ai-syllabus.md         # Giáo trình ISTQB AI Testing tham khảo
│   ├── assignment-policies.md          # Chính sách học vụ môn học
│   └── hw06-team-task-allocation.md    # Bảng phân công nhiệm vụ nhóm
├── test-cases/
│   └── member-1.xlsx                   # File Excel 132 Test Cases & Execution Matrix
├── postman/
│   ├── HW06_API_Testing.postman_collection.json    # Postman Collection v2.1.0 (Sanity + Bug Discovery)
│   ├── HW06_Local.postman_environment.json         # Postman Environment Localhost (Port 3000)
│   ├── HW06_Mock.postman_environment.json          # Postman Environment Mock Server
│   ├── generated_test_suite.json                   # Postman Collection do Agent Skill sinh ra
│   └── data/                                       # Dữ liệu Data-Driven Testing (CSV)
├── newman/
│   └── member-1/                       # Các báo cáo thực thi HTML Extra trực quan (100% Pass)
├── agent-skill/
│   ├── SKILL.md                        # Đặc tả Agent Skill G9.5 Create
│   ├── diagram.png                     # Sơ đồ kiến trúc 4 tầng tự thiết kế
│   ├── pseudocode.md                   # Thuật toán Pseudocode chi tiết 4 tầng
│   ├── skill.py / generate_api_tests.py# Mã nguồn Python CLI thực thi pipeline sinh test
│   └── audit_log.md                    # Nhật ký kiểm toán tự động
├── .github/workflows/
│   └── api-tests.yml                   # Pipeline CI/CD GitHub Actions
└── eshop-sut/                          # Mã nguồn SUT backend và đặc tả API phục vụ chạy test
```

---

## 5. Hướng Dẫn Chạy Kiểm Thử Nhanh (Quick Start)

### 5.1 Khởi động SUT Backend
```bash
cd eshop-sut/backend
npm install
node database.js
node server.js
# Backend lắng nghe tại: http://localhost:3000
```

### 5.2 Chạy Toàn Bộ Test Suite bằng Newman CLI
```bash
# 1. Chạy Sanity Suite (Target: 100% Pass - CI Quality Gate)
newman run postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "01_Sanity_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-1/ci-report.html

# 2. Chạy Bug Discovery Suite (Bắt lỗi và lỗ hổng bảo mật của SUT)
newman run postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "02_Bug_Discovery_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-1/bug-discovery-report.html
```

### 5.3 Chạy Bộ Sinh Test Tự Động (Agent Skill CLI)
```bash
python agent-skill/generate_api_tests.py \
  --spec docs/openapi.yaml \
  --student-id 23127205 \
  --output postman/generated_test_suite.json \
  --audit-out agent-skill/audit_log.md
```
