# Spec: HW06 API Testing 100/100 Points Plan (Member 2: Lê Trung Kiên - 23127075)

> **Authority Reference:** `eshop-sut/api_specification.md` & `eshop-sut/README.md`  
> **Backend Base URL:** `http://localhost:3000`  
> **Student Name:** Lê Trung Kiên (MSSV: 23127075 - Thành viên 2)  

---

## 1. Context & EShop SUT Endpoints
- **Pool A: FR-05 - Liệt kê và tìm kiếm sản phẩm:**
  - `GET /api/products` (Hỗ trợ query parameter `?search=keyword`)
  - `GET /api/products/:id`
- **Pool B: FR-08 - Thanh toán / Tạo đơn hàng:**
  - `POST /api/checkout` (Header `Authorization: Bearer <token>`, Body `{"total_amount": 200000, "shipping_address": "..."}`)
- **Pool C: FR-18 - Quản lý đơn hàng Admin:**
  - `GET /api/admin/orders` (Header `Authorization: Bearer <token>` + `role='admin'`)
  - `PUT /api/admin/orders/:id/status` (Body `{"status": "confirmed"}`, Các trạng thái hợp lệ: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`)

---

## 2. Requirement Matrix & Target Points (100/100)

| Category | Component | Required Deliverables | Points |
| --- | --- | --- | ---: |
| **API 1 (FR-05)** | Product Listing & Search (`GET /api/products?search=`) | - Generate >= 35 AI test cases<br>- Audit table with VALID/INVALID/INCOMPLETE + rationale<br>- Human-added >= 5 test cases + reason why AI missed them<br>- Postman requests + Newman HTML execution report<br>- Pre-request header `X-Student-Id: 23127075`<br>- Bug reports in Markdown & GitHub Issues with screenshots | **30** |
| **API 2 (FR-08)** | Checkout & Order Creation (`POST /api/checkout`) | - Generate >= 35 AI test cases<br>- Audit table with VALID/INVALID/INCOMPLETE + rationale<br>- Human-added >= 5 test cases + reason why AI missed them<br>- Postman requests + Newman HTML execution report<br>- Pre-request header `X-Student-Id: 23127075`<br>- Bug reports in Markdown & GitHub Issues with screenshots | **30** |
| **API 3 (FR-18)** | Order Management Admin (`GET/PUT /api/admin/orders`) | - Generate >= 35 AI test cases<br>- Audit table with VALID/INVALID/INCOMPLETE + rationale<br>- Human-added >= 5 test cases + reason why AI missed them<br>- Postman requests + Newman HTML execution report<br>- Pre-request header `X-Student-Id: 23127075`<br>- Bug reports in Markdown & GitHub Issues with screenshots | **30** |
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
│   ├── ai-prompt-sequence.md          (Step-by-step prompt guide per task)
│   └── git-commit-log.txt             (Exported Git commit log text file)
├── postman/
│   ├── HW06_API_Testing.postman_collection.json (Collection with pre-request script)
│   ├── HW06_Local.postman_environment.json   (Environment variables: http://localhost:3000)
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
