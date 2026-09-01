---
name: api-testing-agent
description: Comprehensive expert agent skill for end-to-end API testing automation, multi-dimensional test generation (Domain/BVA, State Transition, OWASP Security, Schema), Postman collection orchestration, Newman headless execution, SUT state isolation, and automated AI audit logging.
---

# API Testing Agent Skill

## 1. Overview & Capability
The `api-testing-agent` is an expert-level test automation skill designed to orchestrate and execute end-to-end API testing workflows on RESTful backends (such as EShop SUT). It integrates OpenAPI 3.0 specification parsing, multi-dimensional heuristic test generation, Postman Collection v2.1.0 compilation, Newman CLI execution with HTML Extra reporting, state isolation with SQLite fixtures, and automated AI audit logging.

> **Design Paradigm:** **AI-Assisted with Human-in-the-Loop (HITL) Verification Gates** — Strictly rejects unverified black-box generation. Every major phase requires human verification, labelling (VALID / INVALID / INCOMPLETE), and approval checkpoints.

---

## 2. Core Architecture & Toolset

```text
.agents/skills/api-testing-agent/
├── SKILL.md                          <-- Skill specification & AI guidance
└── scripts/                          <-- Modular executable automation toolset
    ├── generate_api_tests.py         <-- Layer 1-4 Heuristic OpenAPI Test Generator (G9.5 Create)
    ├── generate_pdf.py               <-- High-fidelity Markdown to PDF Converter (Playwright + UTF-8)
    ├── smoke_test_sut.py             <-- Pre-flight API health checker for target endpoints
    ├── reset_lockout.py              <-- Clears locked_until and login_attempts in SQLite database
    ├── audit_logger.py               <-- Automatically appends interaction logs to ai-audit-report.md
    ├── package_submission.py         <-- One-command submission packager & ZIP validator
    └── verify_hw06.py                <-- Comprehensive automated rubric & deliverables verifier
```

---

## 3. Human-in-the-Loop Verification Gates (Human Checkpoints)

To ensure academic integrity, adhere to Bloom-AI G9.4 (Collaborate) / G9.5 (Create), and prevent undetected AI hallucinations, the agent operates through 4 strict Human Verification Gates:

```text
[ OpenAPI 3.0 Spec ] ──> [ GATE 1: Spec & Schema Audit ] ──> [ Heuristic Engine ]
                                                                     │
[ Newman Test Run ]  <── [ GATE 2: Test Suite Audit ]    <───────────┘
        │
        └──> [ GATE 3: Ground-Truth Defect Verification ] ──> [ GATE 4: Deliverables Review ]
```

### 🔹 Gate 1: Specification & Schema Audit (Human Checkpoint 1)
- **Actor:** Human Tester / Student.
- **Verification Items:**
  1. Verify OpenAPI 3.0 YAML paths, methods, parameters, request bodies, and response schemas.
  2. Verify authentication requirements (JWT Bearer Token vs Public endpoints).
  3. Reject hallucinated endpoints (e.g. Catching non-existent `PUT/DELETE /api/cart` in SUT).
- **Rule:** AI is NOT permitted to generate Postman collections until Gate 1 schema is verified.

### 🔹 Gate 2: Test Case Labelling & Refinement Audit (Human Checkpoint 2)
- **Actor:** Human Tester / Student vs. AI Generated Test Suite.
- **Verification Items:**
  1. Label every AI-generated test case as `VALID`, `INVALID`, or `INCOMPLETE` with specific technical rationale.
  2. Correct status code assumptions (e.g. SUT returns 401 instead of 400 on unvalidated email format).
  3. Expand the suite with $\ge 5$ Human-Engineered Test Cases covering edge-case state transitions and security negations.

### 🔹 Gate 3: Ground-Truth Defect & Vulnerability Verification (Human Checkpoint 3)
- **Actor:** Human Tester / Student.
- **Verification Items:**
  1. Verify real SUT defects against SRS specification (Logic bugs, missing validation, state pollution).
  2. Perform white-box source code auditing (`server.js`) to pinpoint exact line numbers and root causes.
  3. Verify critical security vulnerabilities (SEC-01 Plaintext Password Leak, SEC-03 Missing Admin Auth).

### 🔹 Gate 4: Continuous Testing Strategy & Deliverables Review (Human Checkpoint 4)
- **Actor:** Human Tester / Student.
- **Verification Items:**
  1. Verify 100% Green run on `01_Sanity_Suite` and defect capture on `02_Bug_Discovery_Suite`.
  2. Verify Anti-fraud headers (`X-Student-Id: {StudentID}`) injected into 100% of requests.
  3. Run `scripts/verify_hw06.py` to ensure 100/100 score across all rubric criteria.

---

## 4. Standard API Testing Workflow

When executing API testing on a target System Under Test (SUT), follow this systematic 6-step procedure:

### Step 1: Pre-Flight Health Check & Database Reset
1. Ensure SUT Backend is active on `http://localhost:3000`.
2. Run database reset to eliminate prior state pollution:
   ```bash
   python scripts/reset_lockout.py
   ```
3. Run smoke test to verify API endpoints:
   ```bash
   python scripts/smoke_test_sut.py
   ```

### Step 2: Automated Test Generation (`generate_api_tests.py`)
Run the 4-layer heuristic engine to parse OpenAPI specification and compile Postman Collection v2.1.0:
```bash
python scripts/generate_api_tests.py \
  --spec docs/openapi.yaml \
  --student-id 23127205 \
  --output postman/generated_test_suite.json \
  --audit-out agent-skill/audit_log.md
```

### Step 3: Test Execution with Newman CLI & HTML Extra Reporter
Execute Sanity Suite and Bug Discovery Suite in headless mode:
```bash
# 1. Sanity Suite (CI Quality Gate - 100% Pass)
newman run postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "01_Sanity_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-1/ci-report.html

# 2. Bug Discovery Suite (Defect Verification)
newman run postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "02_Bug_Discovery_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-1/bug-discovery-report.html
```

### Step 4: High-Fidelity PDF Report Export (`generate_pdf.py`)
Automatically convert all Markdown deliverables into professional A4 PDFs with full Vietnamese UTF-8 typography and embedded Base64 screenshots:
```bash
python scripts/generate_pdf.py --all
```

### Step 5: Verification & Rubric Audit (`verify_hw06.py`)
Run automated validation to verify 100% compliance with HW06 grading rubric:
```bash
python scripts/verify_hw06.py
```

### Step 6: One-Command Submission Packaging (`package_submission.py`)
Compile and validate final ZIP package `<StudentID>_HW06_AI_API_<Grade>.zip`:
```bash
python scripts/package_submission.py
```

---

## 5. Technical Rules & Anti-Fraud Constraints
- **Anti-Fraud Header**: 100% of outgoing Postman requests must inject `X-Student-Id: {StudentID}` via pre-request scripts.
- **State Isolation**: Test fixtures must use independent accounts (`lockout_target@eshop.com`, `admin@eshop.com`, `test@eshop.com`) to prevent domino test failures.
- **Dual-Suite Strategy**: Never mix defect verification tests into the CI Sanity Suite; maintain separate folders `01_Sanity_Suite` (100% Green) and `02_Bug_Discovery_Suite` (Defects).
