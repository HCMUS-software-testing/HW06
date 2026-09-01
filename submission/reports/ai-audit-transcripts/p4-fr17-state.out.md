AI output (rút gọn — Coupon Lifecycle & State Transition)

S1: Admin POST tạo coupon thành công (Mã NEWCOUPON) -> Trạng thái ACTIVE (200)
S2: Public GET /api/coupons -> Mã NEWCOUPON xuất hiện trong danh sách (200)
S3: User POST /api/apply-coupon nhiều lần cho tới khi max_uses = 0 -> Chuyển sang DELETED/EXHAUSTED
S4: Admin DELETE /api/admin/coupons/:id -> Chuyển sang DELETED (200)
S5: GET /api/coupons sau khi xóa -> Mã đã bị xóa không còn xuất hiện trong list (200)
S6: DELETE lại coupon vừa xóa -> Kỳ vọng 404 Not Found (SUT vi phạm trả 200)

Ghi chú người (REVISE): AI không nhận ra bug DELETE coupon đã xóa vẫn trả 200. Đã ghi nhận bug BUG-M3-012.
