# Báo cáo CI/CD

Workflow: `.github/workflows/hw06-23127326.yml`.

## Cấu hình

GitHub Actions kiểm tra secret `STUDENT_ID=23127326`, checkout bài nộp, clone SUT tại commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`, cài dependency backend, khởi động server SQLite sạch, chờ `GET /api/products`, chạy Newman và upload minh chứng JSON/HTML kể cả khi bước test fail.

Chế độ mặc định khi push là `full-pass`. Workflow áp dụng artifact `ci/sut-conformance-fixes.patch` vào clone SUT tạm thời, sau đó chạy **chính full collection 140 catalogue case**, không chạy collection demo. Lần xác nhận cục bộ: 467 HTTP request, 839 assertion, 0 assertion fail; report được xuất thành `ci-full-pass-report.json` và `ci-full-pass-report.html`.

`workflow_dispatch` có ba lựa chọn: `full-pass`, `ci-demo` và `conformance`. `ci-demo` vẫn giữ collection nhỏ để chứng minh một run pass và một run đúng một controlled failure (22 assertion), nhưng không còn được dùng làm minh chứng “toàn bộ API test cases pass”. `conformance` chạy full collection 140 case trên SUT upstream nguyên bản đã pin; run này vẫn đỏ với 42 catalogue case/63 assertion fail do 10 product defect đã ghi nhận. Tách hai baseline này giúp CI full-pass là regression gate có thể tái lập, còn conformance vẫn trung thực với SUT được giao.

Artifact dùng cho full-pass nằm tại `submit/ci/sut-conformance-fixes.patch`; patch chỉ được áp dụng trong clone `/tmp/eshop-sut` của job và không thay đổi source SUT upstream trong repository bài nộp.

## Các lần chạy đã ghi nhận

Các liên kết dưới đây là run GitHub Actions công khai. Ảnh bắt buộc phải chụp từ đúng các trang này; không dùng thẻ trạng thái dựng sẵn.

Lưu ý về tên lịch sử: các run và ảnh minh chứng được ghi nhận trước khi workflow được đổi tên từ `hw06-member4.yml` sang `.github/workflows/hw06-23127326.yml`, nên giao diện cũ có thể hiển thị “HW06 Member 4 Newman”. Đây là cùng branch/bài nộp và ảnh được giữ nguyên để bảo toàn bằng chứng gốc; workflow hiện tại dùng MSSV `23127326`.

| Minh chứng | Commit | Lần chạy Actions | Kết quả mong đợi | Ảnh chụp |
|---|---|---|---|---|
| Full 140-case pass gate | [`9958697`](https://github.com/HCMUS-software-testing/HW06/commit/9958697d6bc7a77583ad95513000d8bfed76dbe6) | [33604168558](https://github.com/HCMUS-software-testing/HW06/actions/runs/33604168558) | 467 request; 839 assertion; **0 assertion fail** | Actions run + `ci-full-pass-report.html` |
| CI demo pass | [`90c2b7e`](https://github.com/HCMUS-software-testing/HW06/commit/90c2b7e6ff1cadd24f9d72300de34b646050cdba) | [33498533231](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498533231) | 22/22 assertion pass | ![CI demo pass](evidence/github-actions-pass.png) |
| CI demo đúng một failure | [`10e32d8`](https://github.com/HCMUS-software-testing/HW06/commit/10e32d8) | [33498587297](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498587297) | 21 pass, đúng 1 controlled assertion fail | ![CI demo failure](evidence/github-actions-one-fail.png) |
| Nhánh xanh khôi phục | [`b0b3764`](https://github.com/HCMUS-software-testing/HW06/commit/b0b3764) | [33498661968](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498661968) | 22/22 assertion pass | cùng trang run trực tiếp |
| Conformance đầy đủ | [`b0b3764`](https://github.com/HCMUS-software-testing/HW06/commit/b0b3764) | [33498724665](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498724665) | 467 request; 839 assertion; 63 assertion sản phẩm fail | ![Full conformance](evidence/github-actions-full-conformance.png) |
