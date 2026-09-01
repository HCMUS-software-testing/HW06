# Báo Cáo CI/CD Pipeline (GitHub Actions & Newman)

## 1. Cấu Hình Pipeline
- **Công cụ:** GitHub Actions workflow (`.github/workflows/newman-api-tests.yml`)
- **Môi trường:** Ubuntu Latest, Node.js v18+, Newman, Newman HTML Extra Reporter
- **Các bước thực thi:**
  1. Checkout repository code.
  2. Khởi chạy SUT EShop trên không gian CI runner (Docker Compose / Node.js).
  3. Cài đặt Newman và các reporters.
  4. Thực thi bộ Postman Collection với môi trường test.
  5. Xuất và lưu trữ Newman HTML report dưới dạng GitHub Actions Artifacts.

---

## 2. Kết Quả Chạy Pipeline Mẫu

### 2.1. Pipeline Run Pass Toàn Bộ
- **Commit:** `test(ci): verify full passing API test suite`
- **Kết quả:** All API tests PASSED.
- **Link & Ảnh màn hình:** `[TODO: Link to passing GitHub Actions run]`

### 2.2. Pipeline Run Fail Có Chủ Đích
- **Commit:** `test(ci): demonstrate intentional failing test assertion`
- **Kết quả:** 1 test case FAILED (AssertionError).
- **Link & Ảnh màn hình:** `[TODO: Link to failing GitHub Actions run]`
