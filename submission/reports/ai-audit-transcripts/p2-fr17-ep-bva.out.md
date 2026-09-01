AI output (rút gọn — 16 partition cho Coupon CRUD)

code:
- P1 valid string ("SUMMER2026") -> hợp lệ
- P2 rỗng "" -> 400
- P3 chứa khoảng trắng ("SUMMER 2026") -> 400
- P4 ký tự đặc biệt XSS `<script>` -> 400 hoặc sanitize
- P5 trùng mã đã có -> 409

discount_type & discount_value:
- P6 type="percent", value=15 (1-100) -> 200 (biên trong)
- P7 type="percent", value=0 -> 400 (biên dưới invalid)
- P8 type="percent", value=100 -> 200 (biên trên valid)
- P9 type="percent", value=101 -> 400 (biên trên invalid)
- P10 type="fixed", value=50000 -> 200
- P11 type="fixed", value=-1000 -> 400

min_order & max_uses:
- P12 min_order=0 -> 200
- P13 min_order âm (-50000) -> 400
- P14 max_uses=1 -> 200
- P15 max_uses=0 -> 400

expired_at:
- P16 ISO date tương lai -> 200
- P17 ISO date quá khứ -> 400

Ghi chú người (REVISE): AI giả định SUT validate percent > 100 và percent <= 0. SUT thực tế chấp nhận percent=1000 và percent=0 mà không báo lỗi. Đã bổ sung kịch bản kỳ vọng theo spec oracle.
