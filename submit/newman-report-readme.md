# Minh chứng Newman

Commit SUT: `85af3ba875c88283615e22cb108f13e2fccaf0e9`. Host: `http://localhost:3000`. MSSV: `23127326`.

## Lần chạy conformance đầy đủ

- Tệp: `newman-full-report.html` / `.json`
- 142 item trong collection (2 setup + 140 catalogue)
- 467 HTTP request, gồm fixture cô lập và postcondition
- 839 assertion: 776 pass, 63 fail
- Kết quả catalogue: 98 PASS, 42 FAIL
- Lỗi fixture/request: 0
- Phân loại: 10 lỗi gốc duy nhất của sản phẩm

## Lần chạy FR-04 theo dữ liệu phone

- Tệp: `newman-report.html` / `.json`
- Dữ liệu: `postman/data/fr04-phone-partitions.csv`
- 6 iteration, 12 request, 18 assertion
- 14 pass, 4 fail; cả bốn failure đều tái hiện việc chấp nhận phone không hợp lệ (`BUG-FR04-03`)

Pre-request script ở cấp collection tự chèn và ghi log `X-Student-Id`. Ảnh chống gian lận vẫn phải chụp từ Postman Console thật; report máy đọc/HTML không thay thế ảnh đó.
