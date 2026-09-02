# HW06 Submission Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an evidence-backed HW06 submission for FR-05, FR-08, and FR-18 whose audited cases, executable Postman assertions, Newman results, reports, and Git history agree.

**Architecture:** Treat the Markdown case inventory as the source of test intent, the Postman collection and data files as the executable layer, and Newman JSON as the source of execution totals. A repository validator enforces IDs, endpoints, traceability, evidence markers, and secret hygiene; report/XLSX/PDF generation consumes those authoritative artifacts instead of duplicating hand-entered counts.

**Tech Stack:** Markdown, Postman Collection v2.1 JSON, Newman, `newman-reporter-htmlextra`, Node.js 22 built-in test runner, ExcelJS, Marked, headless Google Chrome, GitHub Actions, Bash/Git.

**Spec:** `docs/superpowers/specs/2026-09-02-hw06-submission-completion-design.md`

## Global Constraints

- The selected features are FR-05 (`GET /api/products[?search=...]`), FR-08 (`POST /api/checkout`), and FR-18 (`GET /api/admin/orders`, `PUT /api/admin/orders/:id/status`).
- Keep all coursework deliverables under `src/`; root-level tooling and `.github/workflows/` may support those deliverables.
- Preserve the current user edits in `src/README.md`; do not modify or stage `IMPLEMENTATION_PLAN.md`.
- Preserve the 35 original AI-generated cases per FR as provenance, but give every `INVALID` or `INCOMPLETE` case one deterministic correction or an explicit exclusion from the executable scope.
- Do not count FR-06 product-detail behavior as FR-05; replace such final cases with list/search behavior while retaining the original text in the provenance section.
- Every automated assertion name starts with its exact test-case ID, for example `TC-FR08-AI-014 | rejects client total_amount`.
- Never commit JWTs, private credentials, fabricated Newman/CI output, screenshots, issue URLs, backdated commits, or an AI-generated replacement for the student-designed diagram.
- Use the public EShop seed accounts only as documented test fixtures; store no returned token in exported environments or reports.
- Derive all executed/pass/fail totals from the latest committed Newman JSON files, not from manually entered numbers.
- Prefix every shell command with `rtk`; use `apply_patch` for hand-edited text/source files.
- Append one truthful AI audit entry for each real prompt session that changes `src/`, preserving the user prompt verbatim.

---

### Task 1: Add deterministic submission validation and local toolchain

**Files:**
- Create: `package.json`
- Create: `package-lock.json`
- Create: `scripts/validate-submission.mjs`
- Create: `scripts/validate-submission.test.mjs`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: files under `src/test-cases/`, `src/postman/`, `src/newman/`, `src/docs/`, and `src/ai-audit/`.
- Produces: `npm run test:validator`, `npm run validate:submission`, `npm run test:api`, and `npm run export:submission`; later tasks rely on the validator's process exit code.

- [ ] **Step 1: Write validator tests before the validator**

  Cover these pure functions with `node:test`: `extractCaseIds(markdown)`, `countAuditLabels(markdown)`, `collectAssertionIds(collection)`, `loadNewmanTotals(paths)`, and `findForbiddenEvidence(text)`. Include fixtures proving that duplicate IDs, stale endpoints (`/api/products/search`, `/api/orders/checkout`), all-zero SHAs, committed Bearer JWTs, and completed claims paired with manual-evidence markers are rejected.

- [ ] **Step 2: Run the unit tests and confirm the expected initial failure**

  Run: `rtk node --test scripts/validate-submission.test.mjs`

  Expected: FAIL because `scripts/validate-submission.mjs` does not exist.

- [ ] **Step 3: Implement the validator with machine-readable failures**

  Export the five tested functions and a CLI `main()`. The CLI must parse both Postman JSON files, require exactly 35 unique `TC-FRxx-AI-*` IDs per FR, require at least five `TC-FRxx-HUMAN-*` IDs per FR, verify one authoritative audit verdict per AI ID, verify every automated ID appears in the collection assertion registry and traceability matrix, check documented endpoints, scan for credential-like JWTs, and compare report totals with Newman JSON when reports exist. Prefix each diagnostic with `ERROR`, `WARNING`, or `OK` and return non-zero only for errors.

- [ ] **Step 4: Define pinned development dependencies and scripts**

  Set `private: true`, `type: module`, and pin exact versions of `newman`, `newman-reporter-htmlextra`, `exceljs`, and `marked`. Define:

  ```json
  {
    "scripts": {
      "test:validator": "node --test scripts/validate-submission.test.mjs",
      "validate:submission": "node scripts/validate-submission.mjs",
      "test:api": "node scripts/run-newman.mjs",
      "export:submission": "node scripts/export-submission.mjs"
    }
  }
  ```

  Add `node_modules/`, temporary HTML, and unredacted local Postman environments to `.gitignore`; do not ignore committed Newman evidence.

- [ ] **Step 5: Install dependencies and verify the validator itself**

  Run: `rtk npm install`

  Run: `rtk npm run test:validator`

  Expected: all validator unit tests PASS. Then run `rtk npm run validate:submission` and save its current failures as the baseline for Tasks 2–7; this repository-level command is expected to fail until those tasks are complete.

- [ ] **Step 6: Commit the tooling only**

  ```bash
  rtk git add package.json package-lock.json scripts/validate-submission.mjs scripts/validate-submission.test.mjs .gitignore
  rtk git commit -m "chore(member-2): add submission validation tooling"
  ```

### Task 2: Consolidate all three audits into authoritative final case inventories

**Files:**
- Modify: `src/test-cases/member-2-fr-05.md`
- Modify: `src/test-cases/member-2-fr-08.md`
- Modify: `src/test-cases/member-2-fr-18.md`
- Create: `src/test-cases/member-2-traceability.md`

**Interfaces:**
- Consumes: EShop requirements `README.md` sections FR-05/08/10/12/18 and `api_specification.md` sections 3.1, 4.3, and 6.2.
- Produces: canonical IDs, final oracles, automation classification (`NEWMAN`, `BROWSER-MANUAL`, `FAULT-INJECTION`, or `EXCLUDED`), and the case-to-assertion mappings consumed by Tasks 3, 4, and 6.

- [ ] **Step 1: Make the current audit defects fail explicitly**

  Run: `rtk npm run validate:submission`

  Expected: FAIL for duplicate placeholder audit tables in FR-05/FR-08, FR-06 endpoints counted under FR-05, ambiguous multi-status oracles, missing corrections, and absent traceability.

- [ ] **Step 2: Normalize each FR document without altering provenance**

  Keep the original 35-case generation table, followed by exactly one audit table with columns `ID`, `Verdict`, `Technical reason`, `Final correction`, and `Execution class`. Remove duplicate `[Manual by user]` audit tables. For every `INCOMPLETE`/`INVALID` row, state one final status/body/state oracle; when the contract does not define one, recast the correction as an invariant such as “status is not 500, response is JSON, and persistent state is unchanged” and identify the observed status separately after execution.

- [ ] **Step 3: Correct FR-05 scope and cross-layer safety cases**

  Retain AI cases 10–15 and 32 as historical FR-06 output, mark their original forms out of FR-05 execution, and provide replacement FR-05 cases using the same IDs for search normalization, duplicate query parameters, percent-decoding, SQLi differential checks, content type, and non-reflection of raw input. Split API safety from browser rendering: Newman verifies that product JSON neither reflects the query nor expands results; browser-manual rows verify safe text rendering, one `<h1>`, loading, and empty state. Keep all ten human IDs and explicitly identify which half of combined API/UI scenarios Newman can execute.

- [ ] **Step 4: Correct FR-08 state and concurrency preconditions**

  Give each case an isolated cart precondition, unique user/session identity where needed, deterministic checkout body, expected response, cart/order postcondition, and server-calculated total oracle. For the ten human cases, document two-session timing with barriers: cart emptied before checkout, last item removed concurrently, two simultaneous checkouts, stale client total, and stock reaching zero. Mark stock-specific checks as `EXCLUDED` only if the SUT has no stock field or mutation endpoint, with that specification gap as the reason; do not claim they ran.

- [ ] **Step 5: Correct FR-18 authorization, transition, and rollback coverage**

  Remove out-of-scope list/detail assumptions, add exact starting state to each transition, require unchanged state after every rejected request, and split malformed JSON from JSON `null`. Keep privilege-escalation chains: profile role mass assignment, forged JWT variants, user token plus admin-looking body, and authorization-before-mutation. Mark deterministic rollback cases `FAULT-INJECTION` when no black-box hook can trigger the named failure; retain them as human-designed tests without adding them to executed totals.

- [ ] **Step 6: Build the traceability matrix**

  Add one row per 120 authored IDs with columns `Case ID`, `Final intent`, `Execution class`, `Postman folder/request or manual procedure`, `Assertion ID`, and `Latest result source`. Use `NOT-RUN-NO-SUT-HOOK` only for honest browser/fault-injection exclusions. For Newman rows, name the exact request and assertion that Task 3 will implement; leave result source as the deterministic target path `src/newman/member-2/<suite>.json`, not a claimed PASS/FAIL value.

- [ ] **Step 7: Verify case counts and commit**

  Run: `rtk npm run validate:submission`

  Expected: case/audit/endpoint checks PASS; collection/Newman/report checks may still fail because later artifacts are not built.

  ```bash
  rtk git add src/test-cases/member-2-fr-05.md src/test-cases/member-2-fr-08.md src/test-cases/member-2-fr-18.md src/test-cases/member-2-traceability.md
  rtk git commit -m "test(member-2): consolidate audited API case inventories"
  ```

### Task 3: Expand the Postman suite with fixtures, data partitions, and ID-level assertions

**Files:**
- Modify: `src/postman/HW06_API_Testing.postman_collection.json`
- Modify: `src/postman/HW06_Local.postman_environment.json`
- Create: `src/postman/data/fr-05-search.json`
- Create: `src/postman/data/fr-08-checkout.json`
- Create: `src/postman/data/fr-18-admin.json`
- Create: `scripts/run-newman.mjs`
- Create: `scripts/run-newman.test.mjs`

**Interfaces:**
- Consumes: case IDs and execution classes from `src/test-cases/member-2-traceability.md`; runtime variables `baseUrl`, `studentId`, `userEmail`, `userPassword`, `adminEmail`, and `adminPassword`.
- Produces: redacted Postman artifacts and `runSuites(options) -> Promise<RunSummary>`; Task 4 persists its reporter output and Task 5 invokes it in CI.

- [ ] **Step 1: Write runner tests before implementation**

  Test that `buildRuns()` returns separate FR-05, FR-08, and FR-18 runs with the correct folder/data pairing; `summarizeRuns()` must aggregate assertion counts and failures without treating skipped manual cases as passes; `redactReport()` must remove `Authorization` values and JWT-shaped strings. Mock Newman callbacks so unit tests require no live SUT.

- [ ] **Step 2: Run the runner tests and confirm the initial failure**

  Run: `rtk node --test scripts/run-newman.test.mjs`

  Expected: FAIL because `scripts/run-newman.mjs` does not exist.

- [ ] **Step 3: Rebuild the collection by responsibility**

  Use folders `00 - Authentication`, `FR-05 - Product Search`, `FR-08 - Checkout`, `FR-18 - Admin Orders`, and `99 - Cleanup`. Keep the collection-level pre-request script that injects `X-Student-Id`; additionally log `CASE_ID=<id> X-Student-Id=<studentId>` without logging authorization. Authentication requests capture user/admin tokens only into in-memory collection variables and tests assert their absence from exported JSON.

- [ ] **Step 4: Implement data-driven deterministic partitions**

  Each JSON row must contain `caseId`, input fields, expected status/invariant, and setup key. FR-05 rows cover empty/whitespace/Unicode/special/long/SQLi/XSS-encoded searches and schema assertions. FR-08 rows define cart contents, checkout body, authentication mode, and expected cart/order mutation. FR-18 rows define token mode, order start state, requested status, and expected final state. Use one assertion per mapped test ID, even when multiple assertions inspect one response.

- [ ] **Step 5: Implement isolated state workflows**

  Register a unique test user from timestamp plus run ID, login, create cart fixtures, capture created order IDs, and query postconditions. For concurrent FR-08 scenarios, issue two `pm.sendRequest` calls behind an explicit callback barrier and assert the allowed invariant: at most one successful order for one cart snapshot, cart ends empty, and no duplicate order amount. For FR-18, create fresh orders through checkout before state transitions; never rely on fixed order ID `1`.

- [ ] **Step 6: Implement the Newman runner and redaction boundary**

  Run each suite with its matching data file and reporters `cli`, `json`, and `htmlextra`. Write raw reports to a temporary directory, redact request/response authorization data and JWT-like values, then atomically write `src/newman/member-2/fr-05.{json,html,txt}`, `fr-08.*`, `fr-18.*`, and `summary.json`. Exit non-zero when Newman reports assertion/request errors but still preserve the redacted evidence.

- [ ] **Step 7: Validate static mappings before contacting the SUT**

  Run: `rtk npm run test:validator`

  Run: `rtk node --test scripts/run-newman.test.mjs`

  Run: `rtk node -e "JSON.parse(require('fs').readFileSync('src/postman/HW06_API_Testing.postman_collection.json')); JSON.parse(require('fs').readFileSync('src/postman/HW06_Local.postman_environment.json'))"`

  Run: `rtk npm run validate:submission`

  Expected: unit tests and JSON parsing PASS; all `NEWMAN` traceability rows resolve to assertion IDs; only missing execution/report artifacts remain.

- [ ] **Step 8: Commit collection, data, and runner**

  ```bash
  rtk git add src/postman scripts/run-newman.mjs scripts/run-newman.test.mjs
  rtk git commit -m "test(member-2): add traceable Postman API workflows"
  ```

### Task 4: Execute Newman against the live SUT and record only reproducible defects

**Files:**
- Create: `src/newman/member-2/fr-05.json`
- Create: `src/newman/member-2/fr-05.html`
- Create: `src/newman/member-2/fr-05.txt`
- Create: `src/newman/member-2/fr-08.json`
- Create: `src/newman/member-2/fr-08.html`
- Create: `src/newman/member-2/fr-08.txt`
- Create: `src/newman/member-2/fr-18.json`
- Create: `src/newman/member-2/fr-18.html`
- Create: `src/newman/member-2/fr-18.txt`
- Create: `src/newman/member-2/summary.json`
- Modify: `src/bug-reports/member-2-bugs.md`

**Interfaces:**
- Consumes: live `http://localhost:3000`, Postman collection/data, and public seed accounts.
- Produces: machine-readable execution truth and defect records consumed by reports and exports.

- [ ] **Step 1: Establish a clean execution baseline**

  Check `rtk curl -fsS http://localhost:3000/api/products`. If unavailable, start the known local EShop backend and wait until this endpoint returns 200. Confirm the committed environment contains no token and the test database can create unique users without reusing prior fixture IDs.

- [ ] **Step 2: Run all automated suites and retain failing evidence**

  Run: `rtk npm run test:api`

  Expected: the runner always writes redacted JSON/HTML/CLI evidence. A non-zero exit is treated as observed SUT behavior to diagnose, not as permission to weaken an assertion.

- [ ] **Step 3: Diagnose each failure against the specification**

  For every failing ID, reproduce it once with the smallest matching Postman request or `rtk curl`, compare it with the exact FR/SEC requirement, and classify it as test defect, fixture contamination, environment fault, or SUT defect. Fix only test/fixture defects, rerun the affected suite, and preserve only the latest complete report set.

- [ ] **Step 4: Write reproducible local bug records**

  For each confirmed SUT defect, record ID, requirement, severity, preconditions, exact request, expected result, actual result, side effects, and the Newman report/assertion path. Put `External issue: MANUAL-EVIDENCE-REQUIRED` and `Screenshot: MANUAL-EVIDENCE-REQUIRED` until the student creates real public evidence. If no defect remains after rerun, state “No reproducible SUT defect found in this run” and cite `summary.json`.

- [ ] **Step 5: Verify evidence integrity and commit**

  Run: `rtk npm run validate:submission`

  Run: `rtk rg -n "Bearer eyJ|\\\"token\\\"\s*:\s*\\\"eyJ" src/newman src/postman`

  Expected: validator execution checks PASS; secret scan returns no matches; each Newman result has localhost/127.0.0.1 hostname and assertion IDs from traceability.

  ```bash
  rtk git add src/newman/member-2 src/bug-reports/member-2-bugs.md
  rtk git commit -m "test(member-2): record verified Newman execution"
  ```

### Task 5: Add a reproducible CI workflow without inventing public runs

**Files:**
- Create: `.github/workflows/newman-api-tests.yml`
- Create: `src/docs/ci-manual-evidence.md`
- Modify: `src/docs/cicd-report.md`

**Interfaces:**
- Consumes: this repository's locked npm dependencies, public EShop SUT repository, and `npm run test:api`.
- Produces: workflow configuration and exact human steps for two real GitHub Actions runs; it does not produce public URLs locally.

- [ ] **Step 1: Add a workflow syntax/static test to the validator**

  Require checkout of both repositories, Node 22, `npm ci` in `eshop-sut/backend` and this repository, background `node server.js`, a bounded health-check loop against `/api/products`, `npm run test:api`, and unconditional artifact upload from `src/newman/member-2/`.

- [ ] **Step 2: Implement the GitHub Actions workflow**

  Use `actions/checkout` for the submission and a second checkout of `ttbhanh/eshop-sut` into `eshop-sut`. Start the backend from `eshop-sut/backend`; pass only documented demo fixture credentials and `X-Student-Id=23127075`; upload reports with `if: always()`. Add concurrency cancellation and a ten-minute timeout so hung security cases cannot consume a runner indefinitely.

- [ ] **Step 3: Replace CI claims with locally verifiable configuration facts**

  Explain trigger, SUT startup, data-driven runs, reporter outputs, failure semantics, and artifact retention in `cicd-report.md`. In `ci-manual-evidence.md`, give exact steps to push a passing commit, capture its URL/screenshot, create a temporary assertion change that fails, push/capture that run, and immediately revert in a third real commit. Do not list either run as completed before the URLs exist.

- [ ] **Step 4: Validate and commit**

  Run: `rtk npm run validate:submission`

  Expected: workflow structure and documentation checks PASS; manual public-run evidence remains explicitly incomplete and does not affect local Newman truth.

  ```bash
  rtk git add .github/workflows/newman-api-tests.yml src/docs/cicd-report.md src/docs/ci-manual-evidence.md scripts/validate-submission.mjs scripts/validate-submission.test.mjs
  rtk git commit -m "ci(member-2): add Newman API test workflow"
  ```

### Task 6: Synchronize reports and generate Excel/PDF deliverables from evidence

**Files:**
- Modify: `src/README.md`
- Modify: `src/docs/main-report.md`
- Modify: `src/docs/ai-critique.md` only if its verified word count is outside 200–300
- Create: `scripts/export-submission.mjs`
- Create: `scripts/export-submission.test.mjs`
- Create: `src/test-cases/23127075-hw06-test-cases.xlsx`
- Create: `src/docs/main-report.pdf`
- Create: `src/docs/ai-critique.pdf`
- Create: `src/docs/cicd-report.pdf`

**Interfaces:**
- Consumes: canonical case Markdown, traceability, Newman `summary.json`, bug report, AI critique, and CI report.
- Produces: consistent human-readable summaries and generated submission formats.

- [ ] **Step 1: Write export parser tests before the exporter**

  Test `parseCaseTables()`, `buildExecutionSummary()`, and `renderReportHtml()` using compact Markdown/Newman fixtures. Assert that the workbook model contains sheets `Summary`, `FR-05`, `FR-08`, `FR-18`, `Audit`, and `Traceability`, and that totals come from Newman results rather than README text.

- [ ] **Step 2: Run exporter tests and confirm the expected initial failure**

  Run: `rtk node --test scripts/export-submission.test.mjs`

  Expected: FAIL because `scripts/export-submission.mjs` does not exist.

- [ ] **Step 3: Complete the Markdown reports with derived counts**

  Correct stale endpoint names, document generation/audit/extension/execution for each FR, list the exact Postman features actually used, link local Newman artifacts and confirmed bugs, and distinguish `authored`, `automated`, `executed`, and `manual/not-runnable` counts. Update the README self-assessment to an evidence-based score and state which external/manual criteria are outstanding. Preserve the user's current README structure and useful text.

- [ ] **Step 4: Implement deterministic workbook and PDF export**

  Use ExcelJS to create styled/frozen/filterable sheets with one row per case and no formulas that depend on external files. Use Marked to render each required Markdown report into a self-contained UTF-8 HTML document, then invoke `/usr/bin/google-chrome --headless --no-sandbox --print-to-pdf=<target>` for PDF output. Stamp exports with source Git SHA and Newman run timestamp from evidence; do not stamp an invented execution date.

- [ ] **Step 5: Generate and inspect outputs**

  Run: `rtk npm run export:submission`

  Run: `rtk node --test scripts/export-submission.test.mjs`

  Run: `rtk file src/test-cases/23127075-hw06-test-cases.xlsx src/docs/main-report.pdf src/docs/ai-critique.pdf src/docs/cicd-report.pdf`

  Expected: exporter tests PASS; `file` identifies one OOXML workbook and three PDF documents; README/main report totals equal `src/newman/member-2/summary.json`.

- [ ] **Step 6: Commit reports and generated formats**

  ```bash
  rtk git add src/README.md src/docs/main-report.md src/docs/ai-critique.md src/docs/cicd-report.md src/test-cases/23127075-hw06-test-cases.xlsx src/docs/main-report.pdf src/docs/ai-critique.pdf src/docs/cicd-report.pdf scripts/export-submission.mjs scripts/export-submission.test.mjs
  rtk git commit -m "docs(member-2): complete evidence-backed HW06 reports"
  ```

### Task 7: Finalize the Agent Skill narrative and truthful AI audit

**Files:**
- Modify: `src/agent-skill/pseudocode.md`
- Modify: `src/agent-skill/skill-demo-notes.md`
- Preserve unchanged: `src/agent-skill/diagram.mermaid`
- Modify: `src/ai-audit/ai_audit_report.md`
- Create: `src/ai-audit/ai-audit-report.pdf`
- Modify: `src/docs/ai-prompt-sequence.md`

**Interfaces:**
- Consumes: final case lifecycle and the actual user prompts/tool outputs from this work.
- Produces: reusable generator design narrative, audit disclosure, and PDF appendix.

- [ ] **Step 1: Strengthen the pseudocode around review gates**

  Specify functions and data flow for parsing API/FR/SEC contracts, domain partitions, schema assertions, state-machine paths, authorization abuse cases, deduplication by semantic signature, human `VALID/INVALID/INCOMPLETE` review, correction/exclusion, traceability export, and execution-result ingestion. Require human approval before any generated case becomes final or executable.

- [ ] **Step 2: Document what the demo can honestly show**

  Describe inputs, commands, expected generated artifacts, limitations, and a recording checklist. Keep `Video URL: MANUAL-EVIDENCE-REQUIRED` unless a real recording exists. Do not edit or regenerate `diagram.mermaid`; require the student to confirm authorship and export `diagram.png` manually.

- [ ] **Step 3: Reconcile prompts and append one real session entry**

  Keep earlier prompts unchanged, remove duplicate numbering only where the existing audit structure requires reconciliation, and do not invent intermediate conversations. Run the repository's audit append script once with the exact user prompt that authorized this implementation and a factual multi-file output summary. Leave `Verdict`, `Reasoning`, and `Student Fix` for the student as required by the local audit skill.

- [ ] **Step 4: Export and verify the audit appendix**

  Run: `rtk npm run export:submission`

  Confirm the PDF contains sections `1. Thông tin nhóm`, `2. Bảng audit`, `3. Tổng kết độ chính xác AI`, `4. Kết luận`, and `5. Disclosure`; confirm every summary entry has a matching detailed entry and prompts are verbatim.

- [ ] **Step 5: Commit the agent/audit deliverables**

  ```bash
  rtk git add src/agent-skill/pseudocode.md src/agent-skill/skill-demo-notes.md src/ai-audit/ai_audit_report.md src/ai-audit/ai-audit-report.pdf src/docs/ai-prompt-sequence.md
  rtk git commit -m "docs(member-2): finalize agent design and AI audit"
  ```

### Task 8: Regenerate Git evidence and perform the final integrity gate

**Files:**
- Modify: `src/docs/git-commit-log.txt`
- Create: `src/docs/manual-submission-checklist.md`

**Interfaces:**
- Consumes: real repository history and all completed artifacts.
- Produces: final local handoff with no unsupported completion claims.

- [ ] **Step 1: Generate the Git log from real history**

  Replace the fake all-zero SHA file with output equivalent to `git log --date=iso-strict --pretty=format:'%H%x09%ad%x09%an%x09%s'`. Include the design, tooling, audit, Postman, execution, CI, report, and agent/audit commits already created; never hand-type hashes.

- [ ] **Step 2: Create the manual-only submission checklist**

  List exactly these unresolved actions with evidence destinations: confirm/redraw and export `src/agent-skill/diagram.png`; capture Postman console showing `X-Student-Id`; create public GitHub issues/screenshots for confirmed bugs; run and link one passing and one intentionally failing CI commit; record optional Agent Skill video; choose final self-assessed grade; copy `src/` to `23127075_HW06_AI_API_<grade>` and zip only after all chosen evidence is inserted.

- [ ] **Step 3: Run the complete verification gate**

  Run:

  ```bash
  rtk npm run test:validator
  rtk node --test scripts/run-newman.test.mjs scripts/export-submission.test.mjs
  rtk npm run validate:submission
  rtk git diff --check
  rtk rg -n "0000000000000000000000000000000000000000|Bearer eyJ|Link to passing|Link to failing|All API tests PASSED" src .github scripts
  rtk git status --short
  ```

  Expected: all unit/static checks PASS; no forbidden evidence string or token is found; `IMPLEMENTATION_PLAN.md` remains the only unrelated unstaged change; any manual-evidence markers occur only in the checklist, CI handoff, bug report, or demo notes and are never counted as complete.

- [ ] **Step 4: Commit the final generated Git evidence**

  ```bash
  rtk git add src/docs/git-commit-log.txt src/docs/manual-submission-checklist.md
  rtk git commit -m "docs(member-2): finalize submission evidence checklist"
  ```

- [ ] **Step 5: Regenerate the log once after the final commit without creating a self-referential commit claim**

  Regenerate `src/docs/git-commit-log.txt`, verify it includes the final commit, and leave that deterministic refresh clearly reported in the handoff. If a perfectly clean tree is required, create one final `docs(member-2): refresh exported git log` commit and document that the log necessarily ends immediately before its own refresh commit.

