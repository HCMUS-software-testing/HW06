---
name: api-test-generator
description: Generate, audit, extend, and prepare executable API test cases from an API specification and requirements.
---

# AI-guided API test generator

## Purpose

Generate a reviewable API test catalogue for selected features of a backend SUT. The generator must expose its reasoning inputs and leave a human approval gate before any test is executed.

## Inputs

- API specification or endpoint contract.
- SRS/feature requirements and applicable security requirements SEC-01–SEC-07.
- The selected feature and API endpoint(s).
- Optional fixture, authentication, environment, and data-file information.

## Workflow

1. Normalize the selected endpoint contract: method, path parameters, headers, authentication, request body, response schema, status codes, and state effects. Reject an incomplete contract instead of inventing undocumented behavior.
2. Run four coverage planners from the normalized contract:
   - domain planner: boundary, equivalence partitions, type/null/empty, and malformed values for every parameter;
   - state planner: valid, backward, skip, replay, terminal, ownership, and role transitions where the feature changes state;
   - security planner: authentication, authorization, IDOR, injection, XSS handling, mass assignment, sensitive-data exposure, and applicable SEC requirements;
   - schema planner: exact response fields, types, required/optional fields, headers, and absence of secrets.
3. Generate candidate cases with deterministic IDs, isolated preconditions, request data, exact expected status, oracle/schema, and postcondition. Target at least 35 cases for each selected API.
4. Deduplicate candidates and critic-review them for executable setup, observable oracles, requirement mapping, and contradictions. Put uncertain cases in the review queue.
5. Stop at the human review gate. For every generated case, assign `VALID`, `INVALID`, or `INCOMPLETE`, record the reason, and record any correction. Only approved cases may proceed.
6. Add at least five student-authored cases per selected API, prioritizing security and state gaps. Mark them `HUMAN` and explain why the generator missed them.
7. Export the approved catalogue to CSV/XLSX and map it to a Postman collection. Preserve the audit fields and stable case IDs in every export.
8. Execute through Newman (or an equivalent runner) with the required student header, fixtures, exact assertions, schema checks, and postconditions. Record pass/fail results and evidence links.
9. Classify repeated assertion failures into root defects, then produce bug reports only for reproducible SUT defects. Feed execution and audit gaps back into planner rules for the next generation.

## Required output

- Audited catalogue conforming to `references/test-case-schema.md`.
- Postman collection/environment or equivalent executable suite.
- Execution report and failure classification.
- Human-added-case rationale and bug-evidence mapping.
- Prompt/rule refinement notes when a case was rejected or missed.

## Safety and quality gates

- Never claim a case passed without an execution result.
- Never convert an undocumented assumption into an expected oracle without human approval.
- Keep negative tests as valid catalogue cases; a product response contrary to the oracle is a test failure, not an expected pass.
- Do not count repeated assertions for one root cause as separate defects.
- Keep the self-designed diagram and pseudocode as student-owned design evidence; this skill only documents the reusable generator workflow.
