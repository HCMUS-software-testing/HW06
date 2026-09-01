# AI Audit Report — Member 4 (23127326)

## Declaration

I use AI tools for the following tasks: requirement extraction, contract and risk analysis, test-case drafting, row-level audit support, fixture/Postman/CI implementation, execution reconciliation and document structuring. The student owns every final oracle, correction, execution and defect decision.

## Interaction log

Timestamps for AI-001–AI-005 are retained from the commits that first recorded their outputs. Complete structured output is in `../test-cases/member-4.json`; it is not replaced by this summary.

### AI-001 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** Extract FR-04, FR-10 and FR-19 endpoint contracts from `api_specification.md` and normative SRS. List actors, inputs, outputs, roles, state graph and relevant SEC rules. Flag unspecified schema/status assumptions.

**AI output:** A normalized inventory of `GET/PUT /api/users/me`, admin/user order-state endpoints, and admin list/delete-user endpoints; actors and status assumptions; mapping SEC-01–SEC-07. It flagged that SEC-07 belongs to FR-03 and that FR-19 exposes no role-update endpoint.

**Human decision:** Accepted endpoint inventory; kept SEC-07 as explicit N/A and prohibited invented endpoints.

### AI-002 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** For FR-04, generate at least 40 distinct API cases. Partition phone/name/address inputs; cover authentication, identity binding, mass assignment, sensitive fields, XSS-safe output and exact response schema. Include precondition, data, expected result, cleanup and traceability.

**AI output:** 40 structured FR-04 candidate rows spanning authentication, domain boundaries, schema, sensitive fields and security. Output IDs and final corrected forms are `FR04-001`–`FR04-040` in the JSON catalogue.

**Human decision:** Rewrote generic fixtures and alternative statuses into isolated setup, exact integer status and postconditions; retained all 40 as VALID after correction.

### AI-003 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** For FR-10, generate a complete 5×5 state transition matrix plus cancellation, ownership, role, replay, malformed-status, terminal-state and schema cases. Do not invent endpoints.

**AI output:** 45 FR-10 candidate rows containing all source/destination combinations and security/schema variants (`FR10-001`–`FR10-045`).

**Human decision:** Bound each transition to its own order fixture, verified the normative state graph and added GET postconditions before marking VALID.

### AI-004 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** For FR-19, generate at least 40 cases for list/delete only. Cover admin authorization, IDOR, self-delete, invalid IDs, SQL-injection payloads, privacy and schema. Mark role-update ideas out of contract.

**AI output:** 40 list/delete cases (`FR19-001`–`FR19-040`) with negative ID, role, privacy and postcondition ideas.

**Human decision:** Removed non-endpoint ideas, gave destructive cases disposable users and placed self-delete last; all 40 final rows are VALID.

### AI-005 — Codex — 2026-08-31 23:31:31 +07:00

**Prompt:** Audit every generated row as VALID/INVALID/INCOMPLETE with reason; correct invalid/incomplete rows; deduplicate; then add five human cases per feature that are genuinely absent and explain why AI missed them. Compile the approved catalogue into Postman/Newman.

**AI output:** Row-level labels/reasons/corrections plus 15 separate `HUMAN-001` rows. Initial automation exposed ambiguous statuses and shared mutable fixtures.

**Human decision:** Resolved every ambiguity from the normative SRS, repaired fixtures, added exact status/schema/state assertions, and accepted the final 140/140 rows as VALID (125 AI + 15 HUMAN).

### AI-006 — Codex — 2026-09-01 17:30:59 +07:00

**Prompt:** “Hãy xem xét những thứ và nội dung trong submit còn thiếu gì so với req/2026.HW06.API Testing_Vi.md”; “bạn hãy làm tất cả luôn”; correction: GitHub Issue evidence must be a real screenshot, not a drawn console/card.

**AI output:** Rebuilt the executable 140-case suite; executed 467 full-run requests and 839 assertions; reconciled 98 PASS/42 FAIL into 10 root defects; added a six-row data-driven run; redesigned deterministic pass/exact-one-fail CI; expanded bug register/Issues and removed fabricated screenshot references.

**Human decision:** Accepted code/test/document changes subject to authentic manual screenshots, student-drawn diagram, final PDF/XLSX export and ZIP packaging.

## Output accounting

| Output owner | FR-04 | FR-10 | FR-19 | Total |
|---|---:|---:|---:|---:|
| AI-generated, human-audited | 40 | 45 | 40 | 125 |
| Student-added after audit | 5 | 5 | 5 | 15 |
| Final VALID/executed | 45 | 50 | 45 | 140 |

Every row contains `AI source`, `Audit label`, `Audit reason`, `Corrected version` and, for HUMAN rows, `Why AI missed`. No raw AI row is silently represented as student-authored.
