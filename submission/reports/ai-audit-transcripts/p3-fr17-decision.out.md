AI output (rút gọn — Decision Table tạo Coupon)

| Rule | Code Valid | Type Valid | Value Valid | MinOrder >=0 | MaxUses >0 | Expired Tương Lai | Expected Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | T | T (percent) | T (1-100) | T | T | T | 200 (Created) |
| R2 | T | T (fixed) | T (>0) | T | T | T | 200 (Created) |
| R3 | F (rỗng) | T | T | T | T | T | 400 |
| R4 | T | F ("unknown")| T | T | T | T | 400 |
| R5 | T | T (percent) | F (>100) | T | T | T | 400 |
| R6 | T | T | T | F (<0) | T | T | 400 |
| R7 | T | T | T | T | F (<=0) | T | 400 |
| R8 | T | T | T | T | T | F (Quá khứ) | 400 |

Ghi chú người (ACCEPT): Phân tích bảng quyết định hợp lý, bao phủ hết các lỗi thiếu validate trên SUT.
