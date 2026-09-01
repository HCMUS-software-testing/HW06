AI output (rút gọn — 18 partition, người cắt còn các partition có giá trị phân biệt trên SUT)

name:
- P1 valid chuỗi thường -> 200
- P2 rỗng "" -> 400
- P3 thiếu key -> 400
- P4 rất dài (300 ký tự) -> hợp lệ (spec không chặn) — ghi nhận boundary
- P5 chứa XSS `<script>alert(1)</script>` -> không được trả về nguyên văn trong response

email:
- P6 đúng định dạng, domain thật -> pass validate
- P7 thiếu @ -> 400
- P8 thiếu domain part ("a@") -> 400
- P9 chứa khoảng trắng -> 400
- P10 rỗng -> 400
- P11 thiếu key -> 400
- P12 SQLi `' OR 1=1 --` -> phải 400, không được crash/_dump data
- P13 trùng email đã có -> 409

password (BVA trên độ dài, kết hợp đủ policy):
- P14 length 7, đủ policy -> 400
- P15 length 8, đủ policy -> 200  (biên dưới hợp lệ)
- P16 length 9 -> 200
- P17 length 8 thiếu hoa -> 400
- P18 length 8 thiếu `@$!%*?&` -> 400

Ghi chú người: AI thiếu partition "email khác nhau chỉ vì hoa/thường" (admin@eshop.com vs Admin@eshop.com). Đưa vào human-added H01.
