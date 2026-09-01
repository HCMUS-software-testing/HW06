AI output (rút gọn)

Body: {code, total_amount, user_id?}. Auth: JWT Bearer (C4).
C1 tồn tại + is_active. C2 expired_at chưa qua. C3 total >= min_order. C4 authenticated. C5 uses < max_uses_per_user.
Status: 200 {success, coupon_id, discount_amount, final_amount, message}; 400 expired/below min/max uses; 401 missing JWT; 404 unknown/inactive.
Công thức spec: percent = total * discount_value / 100; fixed = discount_value; final = total - discount.
Người: parser phải bắt "lớn hơn hoặc bằng" từ SRS, không cop `>` từ SUT.
