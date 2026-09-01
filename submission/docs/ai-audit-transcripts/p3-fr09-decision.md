Prompt 3 — FR-09 Decision table (PROMPT)

FR-09 apply-coupon có 5 điều kiện đồng thời:
C1 tồn tại + active, C2 chưa hết hạn, C3 total >= min_order, C4 JWT authenticated, C5 remaining uses.
Làm decision table: mỗi hàng một combination (đủ 5 true; lần lượt từng C false).
Chưa sinh test case ID. Công thức percent theo spec: total * discount_value / 100; fixed = discount_value.
