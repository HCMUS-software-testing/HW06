AI output (rút gọn)

SEC-01 injection: code="' OR 1=1 --" → 400/404, không dump DB.
SEC-02 missing JWT → 401 (C4).
SEC-03 role: apply-coupon không phải admin-only; user token hợp lệ.
SEC-04 XSS trong code không được reflect raw.
SEC-05 IDOR: user_id của người khác trong body.
SEC-06 mass-assign is_active/discount trong body apply phải bị ignore.
SEC-07 oversized total_amount / code dài.

Ghi chú người (REVISE): AI liệt kê IDOR nhưng không nhấn "quota tính cho victim". Human H02. AI không nghĩ omit user_id = bypass C5 (H05) — đây không phải SEC-05 cổ điển nên model bỏ.
