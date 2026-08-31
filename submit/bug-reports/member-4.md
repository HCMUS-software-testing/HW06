# Member 4 Bug Report Register

No final bug is claimed until reproduced against running SUT with Newman/Postman evidence.

| Candidate | Requirement | Reproduction request | Expected | Actual | Status |
|---|---|---|---|---|---|
| BUG-04-001 | FR-04, SEC-06 | Authenticated `PUT /api/users/me` body includes `role: admin` | Role unchanged/rejected | `200 {"message":"Profile updated"}`; follow-up GET shows `role:"admin"` | Confirmed; Issue pending |
| BUG-04-002 | FR-04, SEC-01 | Authenticated `GET /api/users/me` | No password/reset token | Response includes plaintext `password` and `reset_token` | Confirmed; Issue pending |
| CAND-03 | FR-10 | Admin transition `canceled → delivered` | 4xx; state unchanged | Capture response/state | Pending evidence |
| CAND-04 | FR-10 | Owner cancel while order `shipping` | 4xx; state unchanged | Capture response/state | Pending evidence |
| BUG-04-005 | FR-12, FR-19 | User token calls `GET /api/admin/users` | 403 | `200` and full user list returned | Confirmed; Issue pending |
| BUG-04-006 | FR-19 | Admin deletes own ID | 4xx; account remains | `200 {"message":"User deleted"}`; ID 1 absent afterward | Confirmed; Issue pending |

For each confirmed bug create one GitHub Issue with severity, SUT commit, request/response, expected/actual, test ID, screenshot and public URL.
