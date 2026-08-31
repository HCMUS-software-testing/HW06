# HW06 — Member 4 submission package

Status: prepared for MSSV `23127326`.

## Scope

- FR-04 Personal profile: `GET/PUT /api/users/me`
- FR-10 Order state machine: `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`
- FR-19 Admin user management: `GET /api/admin/users`, `DELETE /api/admin/users/:id`

## Current evidence status

| Artifact | Status |
|---|---|
| Test-case workbook/CSV | Draft + audit-ready |
| Postman collection/environment | Configured with MSSV `23127326` |
| Newman report | Rerun with MSSV `23127326` |
| Bug report | 4 defects confirmed locally; GitHub Issue links/screenshots still required |
| CI workflow/report | Template created; requires GitHub branch/secrets |
| AI audit/critique | Draft created; add exact timestamps/screenshots |
| Agent Skill pseudocode | Created |
| Self-drawn diagram | **Must be drawn by student** |
| Demo video | **Student records video** |

PDF reports: `pdf/main-report.pdf`, `pdf/ai-audit-report.pdf`, `pdf/ai-critique.pdf`, `pdf/cicd-report.pdf`.

## Summary target

| Feature | AI generated | Human added | Audited | Executed target |
|---|---:|---:|---:|---:|
| FR-04 | 40 | 5 | 40 | 45 |
| FR-10 | 45 | 5 | 45 | 50 |
| FR-19 | 40 | 5 | 40 | 45 |
| **Total** | **125** | **15** | **125** | **140** |

## Final actions before ZIP

1. Set GitHub Actions `STUDENT_ID` secret to `23127326`.
2. Start SUT from clean database; execute full Newman collection.
3. Capture Postman Console showing `X-Student-Id`.
4. Capture real Newman HTML and screenshots for each GitHub Issue.
5. Draw original Agent Skill diagram; do not submit an AI-generated diagram.
6. Record/upload demo video and add public link.
7. Export PDF reports, update actual pass/fail/bug counts, then run ZIP checklist.

Observed smoke: 10 requests, 10 assertions, 7 passed, 3 failed. Full collection: 150 requests/assertions, 84 passed, 66 failed. Confirmed defects: 4 (FR-04 role mass assignment; FR-04 sensitive profile response; FR-19 regular-user admin list; FR-19 admin self-delete). Full report: `newman/member-4/newman-full-report.html`.
