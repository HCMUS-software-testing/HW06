Prompt 5 — FR-17 Security & Auth (PROMPT)

Phân tích các kịch bản kiểm thử Bảo mật và Phân quyền (SEC-01 đến SEC-07) cho FR-17 Coupon CRUD:
- Authorization: Thiếu token (401), Token của User thường gọi API Admin (403).
- Input Injection: SQL Injection, Cross-Site Scripting (XSS) trên `code`.
- Path traversal & Non-numeric ID trên endpoint `DELETE /api/admin/coupons/:id`.
