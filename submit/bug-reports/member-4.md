# Member 4 Bug Report Register

No final bug is claimed until reproduced against running SUT with Newman/Postman evidence.

| Candidate | Requirement | Reproduction request | Expected | Actual | Status |
|---|---|---|---|---|---|
| BUG-04-001 | FR-04, SEC-06 | Authenticated `PUT /api/users/me` body includes `role: admin` | Role unchanged/rejected | `200 {"message":"Profile updated"}`; follow-up GET shows `role:"admin"` | Confirmed; [Issue #1](https://github.com/HCMUS-software-testing/HW06/issues/1) |
| BUG-04-002 | FR-04, SEC-01 | Authenticated `GET /api/users/me` | No password/reset token | Response includes plaintext `password` and `reset_token` | Confirmed; [Issue #2](https://github.com/HCMUS-software-testing/HW06/issues/2) |
| CAND-03 | FR-10 | Admin transition `canceled → delivered` | 4xx; state unchanged | Full catalogue run could not realize a canceled-order fixture; no standalone reproduction claimed | Fixture blocked; not a confirmed bug |
| CAND-04 | FR-10 | Owner cancel while order `shipping` | 4xx; state unchanged | Full catalogue run could not realize a shipping-order owner fixture; no standalone reproduction claimed | Fixture blocked; not a confirmed bug |
| BUG-04-005 | FR-12, FR-19 | User token calls `GET /api/admin/users` | 403 | `200` and full user list returned | Confirmed; [Issue #3](https://github.com/HCMUS-software-testing/HW06/issues/3) |
| BUG-04-006 | FR-19 | Admin deletes own ID | 4xx; account remains | `200 {"message":"User deleted"}`; ID 1 absent afterward | Confirmed; [Issue #4](https://github.com/HCMUS-software-testing/HW06/issues/4) |

For each confirmed bug create one GitHub Issue with severity, SUT commit, request/response, expected/actual, test ID, screenshot and public URL.
