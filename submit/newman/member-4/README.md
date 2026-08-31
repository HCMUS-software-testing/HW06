# Newman evidence

Local run date: 2026-08-31. SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`. Hostname: `localhost` / `127.0.0.1`.

Current smoke report uses MSSV `23127326`; header appears in HTML/JSON request evidence.

Smoke result: 10 requests, 10 assertions, 7 passed, 3 failed. Full result: 150 requests/assertions, 84 passed, 66 failed. Confirmed failures include FR-04 role mass assignment, FR-19 regular-user admin list authorization and FR-19 admin self-delete; FR-04 sensitive-field exposure was confirmed by direct GET. Current collection contains 150 items. See `newman-report.html`, `newman-full-report.html`, JSON reports and `../../bug-reports/member-4.md`.
