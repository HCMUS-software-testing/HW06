AI output (rút gọn — FR-17 Security Cases)

SEC-01 Unauthenticated:
- POST /api/admin/coupons không có Header Authorization -> 401 Unauthorized
- DELETE /api/admin/coupons/1 không có Header Authorization -> 401 Unauthorized

SEC-03 Privilege Escalation / AuthZ:
- POST /api/admin/coupons truyền Bearer Token của User thường -> 403 Forbidden (SUT bị lỗi SEC-03 nhận token User tạo coupon thật)
- DELETE /api/admin/coupons/1 truyền Bearer Token của User thường -> 403 Forbidden (SUT bị lỗi SEC-03 nhận token User xóa coupon)

SEC-04 / SEC-05 Injection & IDOR:
- POST coupon code = `' OR '1'='1` -> 400 Bad Request / Sanitize
- DELETE /api/admin/coupons/abc (ID dạng string) -> 400 Bad Request

Ghi chú người (REVISE): AI đề xuất kỳ vọng 403 cho SEC-03. SUT thực tế bị lỗ hổng chấp nhận User Token thực hiện lệnh Admin (BUG-M3-011). Đã bổ sung kịch bản Human-added để kiểm toán lỗ hổng này.
