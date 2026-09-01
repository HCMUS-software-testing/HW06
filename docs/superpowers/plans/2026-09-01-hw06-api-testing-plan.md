# HW06 API Testing (100/100 Points) Implementation Plan

> **Authority Source:** Grounded strictly in `eshop-sut/api_specification.md` and `eshop-sut/README.md`. Backend Base URL: `http://localhost:3000`.

**Goal:** Complete all requirements for HW06 API Testing for Member 2 (Lê Trung Kiên - 23127075) across 3 assigned APIs (FR-05: `GET /api/products`, FR-08: `POST /api/checkout`, FR-18: `GET/PUT /api/admin/orders`) and Agent Skill to achieve 100/100 points.

**Architecture:** Standardized test pipeline in `src/` directory covering AI generation, human audit, manual test extension, Postman/Newman automation with `X-Student-Id: 23127075` header, CI/CD GitHub Actions integration, bug reporting, AI critique, and AI test generator Agent Skill.

**Tech Stack:** Postman, Newman, Node.js, GitHub Actions, Markdown, Python (AI audit script), Mermaid.

## Global Constraints

- All deliverables MUST reside strictly inside `src/` (main working directory).
- Student ID `23127075` MUST be sent in `X-Student-Id` header for all Postman/Newman requests.
- Base URL = `http://localhost:3000`.
- Member 2 assigned APIs: FR-05 (`GET /api/products?search=`), FR-08 (`POST /api/checkout`), FR-18 (`GET/PUT /api/admin/orders`).
- Each API requires: >= 35 AI test cases, complete VALID/INVALID/INCOMPLETE audit, >= 5 human-designed test cases, Newman HTML report, and bug issues.
- Agent Skill requires: self-drawn diagram + pseudocode + reusable design notes.

---

### Task 1: SUT Setup Verification & Postman Collection Infrastructure

**Files:**
- Modify: `src/postman/HW06_API_Testing.postman_collection.json`
- Modify: `src/postman/HW06_Local.postman_environment.json`

**Interfaces:**
- Consumes: EShop SUT endpoints (`GET /api/products`, `POST /api/checkout`, `GET/PUT /api/admin/orders`)
- Produces: Executable Postman Collection & Environment with pre-request header `X-Student-Id: 23127075` and `baseUrl=http://localhost:3000`

- [ ] **Step 1: Configure Environment Variables**
  - Set `baseUrl` = `http://localhost:3000`, `studentId` = `23127075`, `userToken`, `adminToken`.
- [ ] **Step 2: Add Collection Pre-request Script for Header Injection**
  - Add JavaScript snippet to set `X-Student-Id: 23127075` header on every request.
- [ ] **Step 3: Commit Infrastructure Setup**
  ```bash
  git add src/postman/
  git commit -m "test(member-2): setup Postman collection and environment infrastructure"
  ```

---

### Task 2: FR-05 (Product Listing & Search) Test Pipeline

**Files:**
- Modify: `src/test-cases/member-2-fr-05.md`
- Modify: `src/postman/HW06_API_Testing.postman_collection.json`
- Create: `src/newman/member-2/FR05_Report.html`

**Interfaces:**
- Consumes: `GET /api/products`, `GET /api/products?search=keyword`, `GET /api/products/:id`
- Produces: 35 AI cases + Audit + 5 Human cases + Newman HTML report

- [ ] **Step 1: AI Test Case Generation (35+ cases)**
  - Generate test cases covering `search` query parameter, product details by ID, edge cases, SQLi/XSS in search, and JSON schema.
- [ ] **Step 2: Perform Manual Audit (VALID / INVALID / INCOMPLETE)**
  - Audit every generated case with explicit rationale and fixes.
- [ ] **Step 3: Add Human-designed Cases (5+ cases)**
  - Add security (SQLi/XSS in search params) and negative boundary cases; explain why AI missed them.
- [ ] **Step 4: Implement & Execute via Newman**
  - Add requests to Postman collection and run Newman to export `src/newman/member-2/FR05_Report.html`.
- [ ] **Step 5: Commit**
  ```bash
  git add src/test-cases/member-2-fr-05.md src/postman/ src/newman/member-2/
  git commit -m "test(member-2): complete FR-05 test generation, audit, extension, and execution"
  ```

---

### Task 3: FR-08 (Checkout & Order Creation) Test Pipeline

**Files:**
- Modify: `src/test-cases/member-2-fr-08.md`
- Modify: `src/postman/HW06_API_Testing.postman_collection.json`
- Create: `src/newman/member-2/FR08_Report.html`

**Interfaces:**
- Consumes: `POST /api/checkout`
- Produces: 35 AI cases + Audit + 5 Human cases + Newman HTML report

- [ ] **Step 1: AI Test Case Generation (35+ cases)**
  - Generate cases covering valid checkout (`total_amount`, `shipping_address`), empty cart, insufficient stock, coupon interaction, unauthenticated access, schema validation.
- [ ] **Step 2: Perform Manual Audit (VALID / INVALID / INCOMPLETE)**
  - Audit all cases and document fixes for invalid/incomplete cases.
- [ ] **Step 3: Add Human-designed Cases (5+ cases)**
  - Add race condition, negative stock/price, and multi-session cart manipulation cases; explain why AI missed them.
- [ ] **Step 4: Implement & Execute via Newman**
  - Run Newman and export `src/newman/member-2/FR08_Report.html`.
- [ ] **Step 5: Commit**
  ```bash
  git add src/test-cases/member-2-fr-08.md src/postman/ src/newman/member-2/
  git commit -m "test(member-2): complete FR-08 test generation, audit, extension, and execution"
  ```

---

### Task 4: FR-18 (Order Management Admin) Test Pipeline

**Files:**
- Modify: `src/test-cases/member-2-fr-18.md`
- Modify: `src/postman/HW06_API_Testing.postman_collection.json`
- Create: `src/newman/member-2/FR18_Report.html`

**Interfaces:**
- Consumes: `GET /api/admin/orders`, `PUT /api/admin/orders/:id/status`
- Produces: 35 AI cases + Audit + 5 Human cases + Newman HTML report

- [ ] **Step 1: AI Test Case Generation (35+ cases)**
  - Generate cases covering admin authorization, status machine (`pending` -> `confirmed` -> `shipping` -> `delivered`, `canceled`), invalid transitions, user access restrictions, schema validation.
- [ ] **Step 2: Perform Manual Audit (VALID / INVALID / INCOMPLETE)**
  - Audit all cases with rationale.
- [ ] **Step 3: Add Human-designed Cases (5+ cases)**
  - Add privilege escalation (regular user calling admin endpoint), IDOR on status updates, invalid backward state transitions from `delivered` / `canceled`; explain AI limitations.
- [ ] **Step 4: Implement & Execute via Newman**
  - Export `src/newman/member-2/FR18_Report.html`.
- [ ] **Step 5: Commit**
  ```bash
  git add src/test-cases/member-2-fr-18.md src/postman/ src/newman/member-2/
  git commit -m "test(member-2): complete FR-18 test generation, audit, extension, and execution"
  ```

---

### Task 5: Agent Skill (AI Test Generator) Design & Implementation

**Files:**
- Create/Modify: `src/agent-skill/diagram.mermaid`
- Create/Modify: `src/agent-skill/pseudocode.md`
- Create/Modify: `src/agent-skill/skill-demo-notes.md`

**Interfaces:**
- Consumes: API specification file
- Produces: Self-drawn design diagram + 4-stage pipeline pseudocode + Agent Skill notes

- [ ] **Step 1: Finalize Self-Drawn Diagram**
  - Verify Mermaid diagram source covering API parsing, domain, state, security, schema, and auto-audit stages.
- [ ] **Step 2: Write Pseudocode & Architectural Specification**
  - Detail function definitions, prompting strategies, and JSON schema output format in `src/agent-skill/pseudocode.md`.
- [ ] **Step 3: Document Skill Usage & Demo Notes**
  - Document reusable Agent Skill usage and demo video notes in `src/agent-skill/skill-demo-notes.md`.
- [ ] **Step 4: Commit Agent Skill**
  ```bash
  git add src/agent-skill/
  git commit -m "feat(member-2): design AI Test Generator Agent Skill with diagram and pseudocode"
  ```

---

### Task 6: CI/CD Pipeline, Bug Reports, AI Critique & Final Report Integration

**Files:**
- Create/Modify: `src/docs/main-report.md`
- Create/Modify: `src/docs/ai-critique.md`
- Create/Modify: `src/docs/cicd-report.md`
- Create/Modify: `src/docs/git-commit-log.txt`
- Create/Modify: `src/bug-reports/member-2-bugs.md`
- Create/Modify: `src/README.md`

**Interfaces:**
- Consumes: All execution evidence, bug reports, and commit logs
- Produces: Complete submission package in `src/` ready for 100/100 evaluation

- [ ] **Step 1: Finalize Bug Reports & GitHub Issues**
  - Log all genuine bugs found in `src/bug-reports/member-2-bugs.md` with screenshots.
- [ ] **Step 2: Finalize CI/CD Report**
  - Configure GitHub Actions workflow running Newman; document 1 passing run and 1 failing run in `src/docs/cicd-report.md`.
- [ ] **Step 3: Write AI Critique (200-300 words)**
  - Complete paragraph analyzing AI failures, biases, and lessons learned in `src/docs/ai-critique.md`.
- [ ] **Step 4: Export Git Commit Log & Finalize README.md**
  - Export commit log to `src/docs/git-commit-log.txt`. Update `src/README.md` self-assessment (100/100) and test execution summary table.
- [ ] **Step 5: Final Commit**
  ```bash
  git add src/
  git commit -m "docs(member-2): complete HW06 main report, AI critique, CI/CD report, and self-assessment"
  ```
