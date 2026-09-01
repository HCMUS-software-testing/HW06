AI output (rút gọn)

GET /api/coupons — admin list, 200 array / 401 / 403.
POST /api/admin/coupons — required: code, type ∈ {percent,fixed}, discount_value > 0, expired_at; optional min_order_amount ≥ 0, max_uses_per_user ≥ 1. 200 / 400 / 401 / 403 / 409 duplicate.
DELETE /api/admin/coupons/:id — 200 / 401 / 403 / 404.
Người (REVISE): spec ghi GET dưới /api/admin/coupons ở một chỗ, SUT expose /api/coupons. Ghi nhận path mismatch cho human H01. authenticateToken không check role → SEC-03.
