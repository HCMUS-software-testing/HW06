# Spec: HW06 API Testing 100/100 Points Plan (Member 2: Lê Trung Kiên - 23127075)

## 1. Context & Objectives
- **Student Name:** Lê Trung Kiên
- **Student ID:** 23127075
- **Role:** Member 2
- **Assigned APIs:**
  1. **Pool A:** FR-05 - Liệt kê và tìm kiếm sản phẩm (`GET /api/products`, `GET /api/products/search`)
  2. **Pool B:** FR-08 - Thanh toán / tạo đơn hàng (`POST /api/orders/checkout`)
  3. **Pool C:** FR-18 - Quản lý đơn hàng admin (`GET /api/admin/orders`, `PUT /api/admin/orders/{id}/status`)

---

## 2. Requirement Matrix & Target Points (100/100)

| Category | Component | Required Deliverables | Points |
| --- | --- | --- | ---: |
| **API 1 (FR-05)** | Product Listing & Search | - Generate >= 35 AI test cases<br>- Audit table with VALID/INVALID/INCOMPLETE + rationale<br>- Human-added >= 5 test cases + reason why AI missed them<br>- Postman requests + Newman HTML execution report<br>- Pre-request header `X-Student-Id: 23127075`<br>- Bug reports in Markdown & GitHub Issues with screenshots | **30** |
| **API 2 (FR-08)** | Checkout & Order Creation | - Generate >= 35 AI test cases<br>- Audit table with VALID/INVALID/INCOMPLETE + rationale<br>- Human-added >= 5 test cases + reason why AI missed them<br>- Postman requests + Newman HTML execution report<br>- Pre-request header `X-Student-Id: 23127075`<br>- Bug reports in Markdown & GitHub Issues with screenshots | **30** |
| **API 3 (FR-18)** | Order Management Admin | - Generate >= 35 AI test cases<br>- Audit table with VALID/INVALID/INCOMPLETE + rationale<br>- Human-added >= 5 test cases + reason why AI missed them<br>- Postman requests + Newman HTML execution report<br>- Pre-request header `X-Student-Id: 23127075`<br>- Bug reports in Markdown & GitHub Issues with screenshots | **30** |
| **Agent Skill** | AI-Driven Test Generator | - Self-drawn diagram (Mermaid + PNG)<br>- Comprehensive pseudocode & architectural design<br>- Reusable Agent Skill implementation & demo notes | **10** |
| **Total** | | | **100** |

---

## 3. Deliverable Directory Map (`src/`)

```text
src/
├── README.md                          (Main README with Self-Assessment Table & Test Execution Summary)
├── docs/
│   ├── main-report.md                 (Main HW06 API testing report)
│   ├── ai-critique.md                 (200-300 word AI Critique)
│   ├── cicd-report.md                 (CI/CD GitHub Actions workflow report)
│   └── git-commit-log.txt             (Exported Git commit log text file)
├── postman/
│   ├── HW06_API_Testing.postman_collection.json (Collection with pre-request script)
│   ├── HW06_Local.postman_environment.json   (Environment variables)
│   └── data/                          (Data-driven run files)
├── newman/
│   └── member-2/                      (Newman HTML execution reports)
├── test-cases/
│   ├── member-2-fr-05.md              (Test cases & audit for FR-05)
│   ├── member-2-fr-08.md              (Test cases & audit for FR-08)
│   └── member-2-fr-18.md              (Test cases & audit for FR-18)
├── bug-reports/
│   └── member-2-bugs.md               (Bug reports & GitHub Issues screenshots)
├── agent-skill/
│   ├── diagram.png                    (Self-drawn diagram)
│   ├── diagram.mermaid                (Mermaid source for self-drawn diagram)
│   ├── pseudocode.md                  (AI test generator pseudocode & design)
│   └── skill-demo-notes.md            (Agent skill implementation & demo notes)
└── ai-audit/
    └── ai_audit_report.md             (AI audit report log)
```

---

## 4. Execution Stages

### Stage 1: SUT Setup & Postman Infrastructure
- Confirm local SUT EShop server running (`http://localhost:5000` or equivalent).
- Configure Postman Collection & Environment with pre-request script automatically adding `X-Student-Id: 23127075`.

### Stage 2: Test Case Generation & Audit (FR-05, FR-08, FR-18)
- Generate 35+ test cases for each API covering: Domain Partitioning, State Machine Transitions, Security (SEC-01..SEC-07), and Response Schema.
- Audit each test case as `VALID`, `INVALID`, or `INCOMPLETE` with clear justification.
- Design 5+ human-written test cases per API focusing on security/state edge cases and explain why AI missed them.

### Stage 3: Postman Implementation & Newman Execution
- Implement all 120 test cases (40 per API) in Postman collection.
- Execute test collection via Newman command line, generating HTML reports in `src/newman/member-2/`.

### Stage 4: CI/CD Pipeline & GitHub Integration
- Create GitHub Actions workflow running Newman against SUT.
- Capture 1 passing run and 1 intentionally failing run. Document in `src/docs/cicd-report.md`.

### Stage 5: Bug Reporting, AI Critique & Packaging
- Log genuine bugs found in `src/bug-reports/member-2-bugs.md` and GitHub Issues with screenshots.
- Complete 200-300 word AI Critique in `src/docs/ai-critique.md`.
- Finalize `src/README.md` self-assessment (100/100) and export `git-commit-log.txt`.
