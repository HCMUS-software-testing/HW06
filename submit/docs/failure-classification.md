# Newman failure classification — full run

Run: 150 requests/assertions; 66 failed assertions. SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`.

| # | Item | Class | Bug/Reason |
|---:|---|---|---|
| 1 | `FR04 role escalation must reject` | **DEFECT** | `BUG-04-001` — Role mass assignment reproduced; response 200 |
| 2 | `FR19 user list must reject` | **DEFECT** | `BUG-04-005` — Regular user receives 200 admin list |
| 3 | `FR19 self-delete must reject` | **DEFECT** | `BUG-04-006` — Admin self-delete receives 200 and removes self |
| 4 | `FR04-002 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 5 | `FR04-003 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 6 | `FR04-007 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 7 | `FR04-017 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 8 | `FR04-018 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 9 | `FR04-019 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 10 | `FR04-020 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 11 | `FR04-021 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 12 | `FR04-022 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 13 | `FR04-023 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 14 | `FR04-024 — type` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 15 | `FR04-025 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 16 | `FR04-026 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 17 | `FR04-028 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 18 | `FR04-030 — boundary` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 19 | `FR04-031 — type` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 20 | `FR04-032 — type` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 21 | `FR04-033 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 22 | `FR04-034 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 23 | `FR04-035 — security` | **DEFECT** | `BUG-04-001` — Duplicate role assertion; same root defect |
| 24 | `FR10-002 — state-matrix` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 25 | `FR10-005 — state-matrix` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 26 | `FR10-008 — state-matrix` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 27 | `FR10-010 — state-matrix` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 28 | `FR10-014 — state-matrix` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 29 | `FR10-027 — cancel/ownership` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 30 | `FR10-031 — cancel/ownership` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 31 | `FR10-032 — cancel/ownership` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 32 | `FR10-033 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 33 | `FR10-034 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 34 | `FR10-035 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 35 | `FR10-036 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 36 | `FR10-037 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 37 | `FR10-038 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 38 | `FR10-039 — auth-negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 39 | `FR19-002 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 40 | `FR19-003 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 41 | `FR19-004 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 42 | `FR19-005 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 43 | `FR19-015 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 44 | `FR19-016 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 45 | `FR19-017 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 46 | `FR19-018 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 47 | `FR19-019 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 48 | `FR19-020 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 49 | `FR19-021 — repeat` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 50 | `FR19-022 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 51 | `FR19-023 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 52 | `FR19-024 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 53 | `FR19-025 — auth` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 54 | `FR19-026 — idor` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 55 | `FR19-027 — self-delete` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 56 | `FR19-029 — schema` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 57 | `FR19-032 — type` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 58 | `FR19-033 — security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 59 | `FR19-034 — security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 60 | `FR19-037 — authorization` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 61 | `FR19-040 — negative` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 62 | `FR19-041 — human-security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 63 | `FR19-042 — human-security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 64 | `FR19-043 — human-security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 65 | `FR19-044 — human-security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |
| 66 | `FR19-045 — human-security` | **FIXTURE-ISSUE** | `FIXTURE` — Generic token/body/ID or shared mutable order failed to realize declared precondition. |

## Totals

- DEFECT occurrences: **4** (3 unique root defects)
- EXPECTED-NEGATIVE: **0**
- FIXTURE-ISSUE: **62**

Rule: failed assertion against a correctly realized security/business precondition is DEFECT; failure caused by generic catalogue data is FIXTURE-ISSUE. Negative case name alone never makes result EXPECTED-NEGATIVE.
