AI output (rút gọn — 40 AI cases, người audit)

Happy: POST percent hợp lệ → 200 {coupon_id}; POST fixed; GET list admin 200; DELETE id tồn tại 200.
AuthZ: no token 401; user token 403 trên cả 3 method.
Invalid create: empty body 400; negative discount 400; min_order < 0 400; max_uses 0 400; type bogus 400; percent 1000 400; missing code 400; missing expired_at 400; empty code 400; percent 0 400.
Delete: 99999 → 404; id=abc → 400/404.
Duplicate code SAVE10 → 409.
Basic auth header → 403 (không phải Bearer).

Ghi chú người (REVISE):
- AI giả định DELETE missing id = 404 (ORM). SUT luôn 200. Giữ expected 404 trong discovery.
- AI không đề xuất GET /api/admin/coupons (path lệch spec) — human H01.
- AI map duplicate → 409 đúng spec; SUT 500 SQLITE_CONSTRAINT — human H05.
- 1 case INCOMPLETE: FR-17-035 Basic auth — AI ghi 401, SUT 403; sửa expected = 403 vì authenticateToken verify-fail = 403, khớp SEC-03 hole đã biết.
