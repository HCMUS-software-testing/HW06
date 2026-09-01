# Member 4 — Confirmed Bug Register

All findings were reproduced against SUT commit `85af3ba875c88283615e22cb108f13e2fccaf0e9` at `localhost` with MSSV header `23127326`. Newman evidence is in `../newman/member-4/newman-full-report.html`; case-level mapping is in `../docs/failure-classification.md`.

| Bug ID | Sev. | Expected / actual | Failed test IDs | GitHub Issue |
|---|---|---|---|---|
| `BUG-04-001` | Critical | Client cannot update `role`; API returns 200 and persists `admin`. | FR04-033, 034, 045 | [#1](https://github.com/HCMUS-software-testing/HW06/issues/1) |
| `BUG-04-002` | Critical | Profile omits credentials; API exposes plaintext `password` and `reset_token`. | FR04-010 | [#2](https://github.com/HCMUS-software-testing/HW06/issues/2) |
| `BUG-04-003` | High | Invalid phone partitions return 400/no mutation; API returns 200 and persists them. | FR04-014–021 | [#35](https://github.com/HCMUS-software-testing/HW06/issues/35) |
| `BUG-04-004` | High | Empty/null/partial update is validated and preserves omitted fields; API nulls fields or emits inconsistent error. | FR04-028, 029, 041 | [#36](https://github.com/HCMUS-software-testing/HW06/issues/36) |
| `BUG-10-001` | High | `canceled` is terminal; API accepts `canceled → delivered`. | FR10-024 | [#37](https://github.com/HCMUS-software-testing/HW06/issues/37) |
| `BUG-10-002` | High | User cannot cancel `shipping`; API returns 200 and persists canceled. | FR10-028 | [#38](https://github.com/HCMUS-software-testing/HW06/issues/38) |
| `BUG-04-005` | Critical | Admin endpoints require role=admin; regular-user JWT can list/delete users and transition orders. | FR10-034, 047; FR19-004, 029, 031, 041 | [#3](https://github.com/HCMUS-software-testing/HW06/issues/3) |
| `BUG-19-001` | Medium | Malformed/missing/repeated delete returns 400/404; API repeatedly returns 200. | FR19-017–026, 033, 035–038, 042, 043 | [#39](https://github.com/HCMUS-software-testing/HW06/issues/39) |
| `BUG-19-002` | High | Deleted subject's JWT is rejected; old token still receives 200 from `/api/users/me`. | FR19-044 | [#40](https://github.com/HCMUS-software-testing/HW06/issues/40) |
| `BUG-04-006` | High | Current admin cannot self-delete; API returns 200 and removes it. | FR19-045 | [#4](https://github.com/HCMUS-software-testing/HW06/issues/4) |

Each Issue contains summary, expected/actual, affected API, exact test IDs, SUT commit, severity and report path. Screenshots are deliberately not embedded until captured from the real GitHub Issue UI; see `../evidence/README.md`.
