AI output (rút gọn)

SQLite dump: SAVE10 id=1 bị xoá; tồn tại SAVE10 id=11 min_order_amount=1.
Root cause: FR-17-008 (DELETE /api/admin/coupons/1, user token, SUT 200 — chính là BUG-M3-011) xoá SAVE10 gốc; FR-17-010 POST lại SAVE10 với min=1 (200). Sanity sau đó chạy trên DB bẩn → fail.
AI đề xuất KHÔNG đổi expected theo SUT (đổi sẽ giết discovery). instead quy trình:
reseed → discovery (evidence, làm bẩn DB) → reseed → sanity (xanh) → copy ci-report.
Người ACCEPT. Ghi vào CLAUDE.md + cicd-report.

Hệ quả phụ: chính chuỗi này là bằng chứng BUG-M3-017 (xoá → tạo lại mã với tham số khác, áp dụng ngay).
