AI output (rút gọn)

Lifecycle:
1. Create (FR-17) → List → Apply (FR-09) lần 1 → Apply lần 2 (VIP100) → Apply lần 3 = 400 C5.
2. Apply EXPIRED → 400 C2, không phụ thuộc C3.
3. Admin DELETE coupon đang active → apply mã đó → 404 (C1 fail).
4. Coupon inactive is_active=0 → 404.

Ghi chú người (REVISE): AI không nối FR-17 percent=1000 với FR-09 overflow (final_amount âm). Thêm human-added FR-17-H03 + FR-09 overflow. AI cũng không nêu thứ tự kiểm tra expiry vs min-order.
