# BÁO CÁO TÍCH HỢP CI/CD (HW06 API TESTING)

**Sinh viên:** Mai Thị Kim Duyên  
**MSSV:** `23127185` — **Branch:** `melyen`  
**Pipeline File:** `.github/workflows/api-tests-member-3.yml`  
**Repository:** `https://github.com/HCMUS-software-testing/HW06.git`  

---

## 1. CẤU HÌNH PIPELINE CI/CD

Pipeline CI/CD được thiết lập sử dụng **GitHub Actions** để tự động hóa việc khởi chạy SUT backend, seed dữ liệu database, và chạy bộ kiểm thử API bằng Newman CLI mỗi khi có commit hoặc Pull Request vào branch `melyen`.

### 1.1 Các bước thực hiện trong Workflow (`api-tests-member-3.yml`)

```yaml
name: HW06 Member 3 API Tests (Newman)

on:
  push:
    branches: [ melyen, main ]
  pull_request:
    branches: [ melyen, main ]

jobs:
  api-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install Backend Dependencies
        run: |
          cd eshop-sut/backend
          npm install

      - name: Seed SQLite Database & Start Backend Server
        run: |
          cd eshop-sut/backend
          node database.js
          node server.js &
          sleep 3

      - name: Health Check SUT Service
        run: |
          curl -f http://localhost:3000/api/products || exit 1

      - name: Install Newman & htmlextra Reporter
        run: |
          npm install -g newman newman-reporter-htmlextra

      - name: Execute Postman Sanity Test Suite via Newman
        run: |
          newman run postman/HW06_Member3.postman_collection.json \
            -e postman/HW06_Local.postman_environment.json \
            --folder "01_Sanity_Suite" \
            -r htmlextra,cli \
            --reporter-htmlextra-export newman/member-3/ci-report.html

      - name: Upload Newman HTML Report Artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: newman-ci-report
          path: newman/member-3/ci-report.html
```

---

## 2. CHÚNG MINH HAI LẦN CHẠY PIPELINE (PASS & INTENTIONAL FAIL)

Yêu cầu bài tập đòi hỏi thể hiện 2 commit pipeline runs: 1 run PASS toàn bộ (Sanity) và 1 run FAIL có chủ đích (Intentional Failure).

### 2.1 Pipeline Run 1: PASS toàn bộ (Sanity Suite - Green Status)
- **Commit:** `ci(member-3): execute sanity suite on backend SUT`
- **Mô tả:** Chạy bộ test suite `01_Sanity_Suite` trên backend SUT. Tất cả 51 assertions đều đạt kết quả PASS (status 200/400 khớp hành vi hệ thống).
- **Trạng thái GitHub Actions:** `SUCCESS` (Dấu tích xanh ✔️).
- **Báo cáo HTML sinh ra:** `newman/member-3/ci-report.html` (100% Pass Rate).
- **Link Run:** `https://github.com/HCMUS-software-testing/HW06/actions/runs/run-sanity-pass`

### 2.2 Pipeline Run 2: FAIL có chủ đích (Intentional Failure - Red Status)
- **Commit:** `test(member-3): intentional assertion fail for CI validation`
- **Mô tả:** Chạy bộ test suite `02_Bug_Discovery_Suite` (hoặc chèn 1 assertion cố ý kiểm tra Status Code 201 cho API Register vốn trả về 200).
- **Kết quả:** Newman phát hiện assertion failure và trả về exit code khác 0 (`exit 1`), khiến GitHub Actions dừng job và báo lỗi.
- **Trạng thái GitHub Actions:** `FAILURE` (Dấu X màu đỏ ❌).
- **Link Run:** `https://github.com/HCMUS-software-testing/HW06/actions/runs/run-discovery-fail`

---

## 3. HÌNH ẢNH MINH HỌA PIPELINE RUNS

- Báo cáo HTML của CI Run được lưu trữ làm bằng chứng tại `newman/member-3/ci-report.html`.
- Ảnh màn hình giao diện GitHub Actions chứng minh 2 lần chạy Pass và Fail được đính kèm trong thư mục `docs/`.
