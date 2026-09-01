# HW06 — API testing submission package

Status: prepared for MSSV `23127326`.

## Scope

- FR-04 Personal profile: `GET/PUT /api/users/me`
- FR-10 Order state machine: `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`
- FR-19 Admin user management: `GET /api/admin/users`, `DELETE /api/admin/users/:id`

## Current evidence status

| Artifact | Status |
|---|---|
| Test-case workbook/CSV | 140 catalogue-linked cases; Newman result mapping completed |
| Postman collection/environment | Configured with MSSV `23127326` |
| Newman report | Rerun with MSSV `23127326` |
| Bug report | 4 defects confirmed; Issues #1–#4 and evidence links published |
| CI workflow/report | Secret configured; green smoke and red full-conformance runs linked |
| AI audit/critique | Markdown + PDF with interaction log, transcript and critique |
| Agent Skill pseudocode | Created |
| Agent Skill diagram | `agent-skill/diagram.png` + editable SVG/Mermaid source |
| Demo video | **Student records video** |

PDF reports: `pdf/main-report.pdf`, `pdf/ai-audit-report.pdf`, `pdf/ai-critique.pdf`, `pdf/cicd-report.pdf`.

Repository: <https://github.com/HCMUS-software-testing/HW06/tree/Bao>

Student video (to be added by student): `VIDEO_URL_PENDING`

## Summary target

| Feature | AI generated | Human added | Audited | Executed target |
|---|---:|---:|---:|---:|
| FR-04 | 40 | 5 | 40 | 45 |
| FR-10 | 45 | 5 | 45 | 50 |
| FR-19 | 40 | 5 | 40 | 45 |
| **Total** | **125** | **15** | **125** | **140** |

## Test summary

| Metric | Value |
|---|---:|
| Selected APIs | 3 (FR-04, FR-10, FR-19) |
| AI-generated cases | 125 |
| Human-added cases | 15 |
| Executed requests | 150 (140 catalogue + 10 setup/smoke) |
| Passed assertions | 84 |
| Failed assertions | 66 |
| Confirmed defect observations | 4 (4 unique root defects; one direct GET verification) |
| Expected-negative failures | 0 |
| Fixture-issue failures | 62 |

## Self-assessment

| Criterion | Max | Self-assessment |
|---|---:|---:|
| AI-generated/audited/extended test cases | 25 | 24 |
| Postman/Newman execution and evidence | 20 | 17 |
| Real bug reports + GitHub Issues | 15 | 15 |
| CI/CD integration and two runs | 15 | 12 |
| AI Audit Report | 10 | 9 |
| AI Critique (200–300 words) | 5 | 5 |
| Agent Skill (diagram + pseudocode) | 10 | 9 |
| **Total** | **100** | **91** |

## Final actions before ZIP

1. Set GitHub Actions `STUDENT_ID` secret to `23127326`.
2. Start SUT from clean database; execute full Newman collection.
3. Capture Postman Console showing `X-Student-Id`.
4. Capture Postman Console and student-recorded video; replace `VIDEO_URL_PENDING`.
5. Keep GitHub Issue and Actions links/screenshots in `evidence/`.
6. Export PDFs after the final Markdown edit, then run ZIP checklist.

CI smoke gate: 7 requests, 7 assertions, 7 passed. The local 10-item smoke catalogue recorded 7 passed and 3 failed. Full collection: 150 requests/assertions, 84 passed, 66 failed. Confirmed defects: 4 (FR-04 role mass assignment; FR-04 sensitive profile response; FR-19 regular-user admin list; FR-19 admin self-delete). Full report: `newman/member-4/newman-full-report.html`.
