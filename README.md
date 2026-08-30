# HW06 - Kiểm Thử API & Ứng Dụng AI (Software Testing)

## 1. Thông Tin Sinh Viên
- **Họ và tên:** Lâm Hữu Khánh
- **Mã số sinh viên:** 23127205
- **Vai trò trong nhóm:** Thành viên 1
- **Bộ ba API phụ trách:**
  - **Pool A:** FR-02: Đăng nhập & Khóa tài khoản (`POST /api/login`)
  - **Pool B:** FR-07: Giỏ hàng (`GET /api/cart`, `POST /api/cart`)
  - **Pool C:** FR-15: Quản lý sản phẩm CRUD (`POST/GET/PUT/DELETE /api/products`)
- **Repository GitHub:** https://github.com/HCMUS-software-testing/HW06.git
- **Branch nộp bài:** `khanh`

---

## 2. Bảng Tự Đánh Giá Điểm (Self-Assessment Rubric)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá | Minh chứng / Deliverable |
|:---:|---|:---:|:---:|---|
| 1 | **API 1 (FR-02)** — Pipeline toàn bộ (Generate + Audit + Extend + Execute + Bugs) | 30 | 30 | `postman/`, `newman/member-1/fr02-report.html`, `test-cases/member-1.xlsx` |
| 2 | **API 2 (FR-07)** — Pipeline toàn bộ (Generate + Audit + Extend + Execute + Bugs) | 30 | 30 | `postman/`, `newman/member-1/fr07-report.html`, `test-cases/member-1.xlsx` |
| 3 | **API 3 (FR-15)** — Pipeline toàn bộ (Generate + Audit + Extend + Execute + Bugs) | 30 | 30 | `postman/`, `newman/member-1/fr15-report.html`, `test-cases/member-1.xlsx` |
| 4 | **Agent Skill (G9.5 - Create)** — Bộ sinh test API tự động từ API Spec | 10 | 10 | `agent-skill/diagram.png`, `agent-skill/pseudocode.md`, `agent-skill/skill.py` |
| | **TỔNG ĐIỂM** | **100** | **100** | **File nộp: `23127205_HW06_AI_API_100.zip`** |

---

## 3. Báo Cáo Tóm Tắt Kiểm Thử (Test Execution Summary)

| Chỉ số tổng hợp | FR-02 (Login & Lockout) | FR-07 (Cart) | FR-15 (Product CRUD) | TỔNG CỘNG |
|---|:---:|:---:|:---:|:---:|
| **Test Cases AI Sinh ra** | 38 | 38 | 38 | **114** |
| **Test Cases được Audit** | 38 | 38 | 38 | **114** |
| **Test Cases Con người Tự thêm** | 6 | 6 | 6 | **18** |
| **Tổng số Test Cases Thiết kế** | **44** | **44** | **44** | **132** |
| **Test Cases Thực thi trong Sanity Suite** | 30 | 30 | 30 | **90** |
| **Test Cases Pass (Sanity Suite CI)** | 30 | 30 | 30 | **90 (100%)** |
| **Test Cases Bắt Bug (Bug Discovery Suite)** | 14 | 14 | 14 | **42** |
| **Số lỗi thật (Bugs) phát hiện & Báo cáo** | 3 | 3 | 4 | **10 Bugs** |

---

## 4. Hướng Dẫn Chạy Kiểm Thử (Quick Start)

### 4.1 Khởi động SUT Backend
```bash
cd eshop-sut/backend
npm install
node database.js
node server.js
# Server chạy tại http://localhost:3000
```

### 4.2 Chạy Toàn Bộ Test Suite bằng Newman CLI
```bash
# Chạy Sanity Suite (Target: 100% Pass)
newman run postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "01_Sanity_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-1/ci-report.html

# Chạy Bug Discovery Suite (Bắt lỗi SUT)
newman run postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "02_Bug_Discovery_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-1/bug-discovery-report.html
```

---

## 5. Cấu Trúc Thư Mục Bàn Giao
- `docs/`: Báo cáo chính (`main-report.md`, `main-report.pdf`), Báo cáo CI/CD, Phê bình AI, Kiểm toán AI.
- `postman/`: Postman Collection JSON, Environment JSON, Data files CSV.
- `newman/member-1/`: Các báo cáo thực thi HTML Newman.
- `test-cases/`: File Excel `member-1.xlsx` chi tiết 132 Test Cases.
- `bug-reports/`: Báo cáo bug Markdown và ảnh chụp màn hình GitHub Issues.
- `agent-skill/`: Sơ đồ tự vẽ, Pseudocode, mã nguồn Python `skill.py` cho Agent Skill.
- `.github/workflows/`: CI/CD Pipeline workflow GitHub Actions.
