# Báo cáo CI/CD

Workflow: `.github/workflows/hw06-23127326.yml`.

## Cấu hình

GitHub Actions kiểm tra secret `STUDENT_ID=23127326`, checkout bài nộp, clone SUT tại commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`, cài dependency backend, khởi động server SQLite sạch, chờ `GET /api/products`, chạy Newman và upload minh chứng JSON/HTML kể cả khi bước test fail.

Các lần chạy khi push dùng `HW06_23127326_ci_demo_collection.json`. Bộ này gồm các case đại diện đã duyệt cho FR-04, FR-10, FR-19 và một assertion điều khiển pipeline có tên rõ ràng. Khi `ci-force-failure.txt=false`, cả 22 assertion đều pass. Khi đặt `true`, chỉ `CI-DEMO-001 controlled assertion` fail; điều đó chứng minh pipeline phát hiện test đỏ và không quy nhầm thành lỗi SUT.

`workflow_dispatch` thủ công có lựa chọn `conformance`, chạy toàn bộ catalogue 140 case. Run này cố ý đỏ trên SUT lỗi đã pin (42 catalogue case fail); che các failure để CI xanh sẽ làm sai kết quả conformance.

## Các lần chạy đã ghi nhận

Các liên kết dưới đây là run GitHub Actions công khai. Ảnh bắt buộc phải chụp từ đúng các trang này; không dùng thẻ trạng thái dựng sẵn.

| Minh chứng | Commit | Lần chạy Actions | Kết quả mong đợi | Ảnh chụp |
|---|---|---|---|---|
| CI demo pass | [`90c2b7e`](https://github.com/HCMUS-software-testing/HW06/commit/90c2b7e6ff1cadd24f9d72300de34b646050cdba) | [33498533231](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498533231) | 22/22 assertion pass | ![CI demo pass](evidence/github-actions-pass.png) |
| CI demo đúng một failure | [`10e32d8`](https://github.com/HCMUS-software-testing/HW06/commit/10e32d8) | [33498587297](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498587297) | 21 pass, đúng 1 controlled assertion fail | ![CI demo failure](evidence/github-actions-one-fail.png) |
| Nhánh xanh khôi phục | [`b0b3764`](https://github.com/HCMUS-software-testing/HW06/commit/b0b3764) | [33498661968](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498661968) | 22/22 assertion pass | cùng trang run trực tiếp |
| Conformance đầy đủ | [`b0b3764`](https://github.com/HCMUS-software-testing/HW06/commit/b0b3764) | [33498724665](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498724665) | 467 request; 839 assertion; 63 assertion sản phẩm fail | ![Full conformance](evidence/github-actions-full-conformance.png) |
