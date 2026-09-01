AI output (rút gọn — người sửa 2 chỗ: C3 inclusive, C4 phải 401)

| C1 | C2 | C3 | C4 | C5 | Spec |
| T | T | T | T | T | 200, discount theo công thức |
| F | - | - | - | - | 404 unknown/disabled |
| T | F | T | T | T | 400 expired |
| T | T | F | T | T | 400 below min |
| T | T | T | F | T | 401 (C4 / SEC-02) |
| T | T | T | T | F | 400 max uses |

BVA C3 cho SAVE10 (min 300000): 299999, 300000, 300001.
Coupon seed: SAVE10 percent 10 min 300000; BIGBUY fixed 50000 min 500000; VIP100 fixed 100000 min 300000 max 2; EXPIRED.

Ghi chú người (REVISE):
1. AI viết C3 là `>` vì nhìn SUT. Spec viết "lớn hơn hoặc bằng". Giữ `>=`.
2. AI đề xuất 403 cho C4. Spec C4 = authenticated → 401 nếu thiếu token.
3. AI không nghĩ tới omit user_id để bypass C5 — đưa vào H05.
