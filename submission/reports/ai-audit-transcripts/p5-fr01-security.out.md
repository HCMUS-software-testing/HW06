AI output (rút gọn)

SEC-01 SQLi email/name → 400 không dump. SEC-04 XSS name không reflect. SEC-06 mass-assign role=admin phải bị ignore (user mới vẫn role user). Public API, không 401. Oversized name 10k chars.
Người (REVISE): AI bỏ Content-Type x-www-form-urlencoded (TypeError 500 — H02) và case-insensitive duplicate email (H01). Mass-assign role AI có, SUT ignore (sanity pass) — giữ VALID.
