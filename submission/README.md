# HW06 — AI-FIRST API TESTING & AGENT SKILL DESIGN

**Môn học:** Kiểm thử Phần mềm (Software Testing) — HW06  
**Sinh viên:** Mai Thị Kim Duyên  
**MSSV:** `23127185` — **Vai trò:** Thành viên 3 — **Branch:** `melyen`  
**Header bắt buộc:** `X-Student-Id: 23127185`  
**Tên file nộp Moodle:** `23127185_HW06_AI_API_100.zip`  
**GitHub Repository:** `https://github.com/HCMUS-software-testing/HW06.git`  
**Target SUT:** EShop Backend API (`http://localhost:3000`)  

---

## 1. BẢNG TỰ ĐÁNH GIÁ (SELF-ASSESSMENT RUBRIC)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá | Ghi chú & Minh chứng |
| --- | --- | ---: | ---: | --- |
| 1 | **API 1 - FR-01 Đăng ký (`POST /api/register`)** | 30 | **30** | 46 cases (40 AI + 6 Human), 3 bugs, Newman HTML report |
| 2 | **API 2 - FR-09 Áp dụng Coupon (`POST /api/apply-coupon`)** | 30 | **30** | 45 cases (40 AI + 5 Human), 7 bugs, Decision Table C1-C5 |
| 3 | **API 3 - FR-17 Quản lý Coupon Admin (`GET/POST/DELETE`)** | 30 | **30** | 46 cases (40 AI + 6 Human), 7 bugs, SEC-03 AuthZ bug |
| 4 | **Agent Skill (G9.5)** — Bộ sinh test API dẫn dắt bởi AI | 10 | **10** | Sơ đồ tự vẽ PNG, Pseudocode MD, Python generator |
| | **TỔNG CỘNG** | **100** | **100** | **Điểm tự đánh giá: 100/100 (File: `23127185_HW06_AI_API_100.zip`)** |

---

## 2. BÁO CÁO TÓM TẮT KIỂM THỬ (TEST SUMMARY COUNTS)

- **Số lượng API thực hiện:** `3` (`FR-01`, `FR-09`, `FR-17`)
- **Số lượng Test Cases do AI tạo:** `120` (40 cases / API)
- **Số lượng Test Cases do Người tạo thêm (Human-added):** `17` (6 FR-01 + 5 FR-09 + 6 FR-17)
- **Tổng số Test Cases:** `137`
- **Số Test Cases được thực thi:** `137`
- **Số Test Cases PASS (Sanity Suite):** `51 / 51` (100% Pass)
- **Số Test Cases FAIL (Bug Discovery Suite):** `69 / 86` (do SUT vi phạm đặc tả Specification)
- **Số lượng Bug phát hiện:** `17` (4 Critical, 5 High, 6 Medium, 2 Low)

---

## 3. CẤU TRÚC THƯ MỤC NỘP BÀI (SUBMISSION LAYOUT)

```text
23127185_HW06_AI_API_100/ (hoặc submission/)
├── reports/
│   ├── main-report.md                          # Báo cáo chính
│   ├── bug-report.md                           # Báo cáo chi tiết 17 bugs phát hiện (gắn link GitHub Issues #18-#34)
│   ├── ai-audit-report.md                      # Nhật ký kiểm toán AI (15 tương tác)
│   ├── ai-critique.md                          # Bài viết Phê bình AI
│   ├── cicd-report.md                          # Báo cáo tích hợp GitHub Actions
│   ├── git-commit-log.txt                      # Log commits theo từng bước
│   └── ai-audit-transcripts/                   # Chi tiết transcripts các phiên prompt
├── test-cases/
│   ├── member-3.xlsx                           # File Excel tổng hợp 137 test cases
│   └── generated/                              # CSV test cases từng API (FR-01, FR-09, FR-17)
├── postman/
│   ├── HW06_Member3.postman_collection.json    # Collection Postman chứa Pre-request Script
│   ├── HW06_Local.postman_environment.json     # Environment local (http://localhost:3000)
│   ├── HW06_Mock.postman_environment.json      # Environment Mock server
│   └── data/                                   # File CSV phục vụ Collection Runner DDT
├── newman/member-3/
│   ├── sanity-report.html                      # Newman HTML report (Sanity Suite - 100% Pass)
│   ├── bug-discovery-report.html               # Newman HTML report (Discovery Suite)
│   └── ci-report.html                          # Newman HTML report CI run
├── bug-reports/
│   ├── member-3.md & member-3.pdf              # Báo cáo chi tiết 17 bugs phát hiện
│   └── (screenshots/issue links)               # Bằng chứng đính kèm
├── agent-skill/
│   ├── SKILL.md                                # Hướng dẫn Agent Skill
│   ├── diagram.png & diagram.svg               # Sơ đồ kiến trúc generator TỰ VẼ
│   ├── pseudocode.md                           # Thuật toán sinh testcases
│   ├── generate_api_tests.py                   # Script sinh test cases Python
│   └── audit_logger.py                         # Tool tự động log AI Audit
├── openapi/
│   └── eshop-member3.yaml                      # OpenAPI 3.0 spec đã kiểm toán
├── .github/workflows/
│   └── api-tests-member-3.yml                  # GitHub Actions workflow
└── README.md                                   # File README chứa bảng tự đánh giá & counts
```

---

## 4. HƯỚNG DẪN CHẠY KIỂM THỬ

### 4.1 Khởi chạy SUT Backend
```bash
cd eshop-sut/backend
npm install
node database.js    # Seed database
node server.js      # Backend chạy tại http://localhost:3000
```

### 4.2 Thực thi Postman Collection qua Newman
```bash
# Sanity Suite (Kỳ vọng 100% PASS)
node eshop-sut/backend/database.js
npx newman run postman/HW06_Member3.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "01_Sanity_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-3/sanity-report.html

# Bug Discovery Suite (Phát hiện lỗi SUT so với Spec)
node eshop-sut/backend/database.js
npx newman run postman/HW06_Member3.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "02_Bug_Discovery_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-3/bug-discovery-report.html
```

---

## 5. CÁC ĐIỀU KIỆN CHỐNG GIAN LẬN (ANTI-CHEAT COMPLIANCE)

1. **Header `X-Student-Id: 23127185`:** Được cài đặt ở Collection-level Pre-request script và log trực tiếp ra Postman Console trong mọi request.
2. **Newman Report Hostname:** Hostname thực thi hiển thị chính xác `http://localhost:3000` trên hệ thống local.
3. **Agent Skill Diagram:** Sơ đồ kiến trúc tại `agent-skill/diagram.png` do người tự vẽ thủ công (không dùng AI sinh ảnh).
