# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

HW06 is an **API testing homework** (not an application to build). The System Under Test is **EShop**, a deliberately buggy Vietnamese e-commerce demo. Work is AI-first but **step-by-step**: generate → human-audit → extend → execute → report bugs. Raw AI output without review is not acceptable.

- Assignment: `req/2026.HW06.API Testing_En.md` (Vietnamese: `req/2026.HW06.API Testing_Vi.md`)
- Team split: `docs/hw06-team-task-allocation.md` (Vietnamese: `docs/hw06-phan-cong-cong-viec-nhom.md`)
- SUT source of truth: https://github.com/ttbhanh/eshop-sut (`api_specification.md` + SRS in that repo)
- Group GitHub: https://github.com/HCMUS-software-testing/HW06.git
- Course treats this as an **individual** submission even though the group shares the repo. Each member owns a unique 3-API triple and keeps their own audit, tests, Newman evidence, bugs, and commit log.

This branch (`melyen`) currently holds only the assignment and the team plan. Member 1 lives on `origin/khanh`; Member 4 lives on `origin/Bao`. Clone or copy SUT/test patterns from those branches — do not reuse their API triples, Student IDs, or prompts.

## Team API ownership (do not collide)

| Member | Branch (as of 2026-09-01) | Pool A | Pool B | Pool C |
| --- | --- | --- | --- | --- |
| 1 — Lâm Hữu Khánh (`23127205`) | `khanh` | FR-02 Login / lockout | FR-07 Cart | FR-15 Product CRUD |
| 2 | (unclaimed here) | FR-05 Product list/search | FR-08 Checkout | FR-18 Admin orders |
| 3 | (unclaimed here) | FR-01 Register | FR-09 Coupons | FR-17 Coupon CRUD |
| 4 — MSSV `23127326` | `Bao` | FR-04 Profile | FR-10 Order state machine | FR-19 Admin users |

Confirm which member this branch is before generating tests. No two members may use the same three-API selection. Copying work **including prompts** scores 0 for both parties.

## Per-API pipeline (repeat for all three APIs)

1. Read the matching endpoints in `api_specification.md` plus SEC-01–SEC-07.
2. Drive AI **step by step** (not one generic prompt) to generate **≥ 35** cases covering domain partitions, state transitions, security, and response schema.
3. Audit every AI case `VALID` / `INVALID` / `INCOMPLETE` with reasoning; fix the bad ones.
4. Add **≥ 5** human cases the AI missed (especially security and state transitions) and explain why they were missed.
5. Implement in Postman. Every request must send `X-Student-Id: {StudentID}` (collection-level pre-request script).
6. Run with Newman; export HTML. Hostname in the report must be the real SUT (`localhost` / `127.0.0.1` is accepted).
7. File genuine bugs in Markdown **and** GitHub Issues with screenshots.
8. Commit after generation, audit, extension, execution, and bug reporting.

Minimum per member: 105 AI cases, 15 human cases, 3 APIs executed, ≥ 12 major commits.

## SUT architecture

EShop is four processes. **This homework targets the backend API only** (Pool D / mobile is out of scope).

| Process | Stack | Default URL |
| --- | --- | --- |
| Backend API | Node.js + Express + SQLite | `http://localhost:3000` |
| Storefront | React + Vite | `http://localhost:5173` |
| Admin | React + Vite | `http://localhost:5174` |
| Mobile | React Native + Expo | device LAN IP |

Canonical seed accounts (SRS / Member 1 seed):

- Admin: `admin@eshop.com` / `Admin123!`
- User: `test@eshop.com` / `Test1234!`

`eshop-sut/setup_guide.md` lists admin password `admin123` — that is **not** the SRS password. Treat spec vs implementation mismatches as potential bugs, not as a reason to silently “fix” the SUT.

JWT is signed with a hardcoded secret in `server.js`. Carts are an in-memory `userCarts` map (lost on restart). SQLite file is `backend/database.sqlite`; re-seed with `node database.js` before lockout/CRUD runs so state does not leak across suites.

Auth header: `Authorization: Bearer <token>`. Admin APIs under `/api/admin/*` plus mutating product/category/coupon routes require `role = 'admin'` per spec (SEC-03). The SUT is **intentionally buggy** (lockout counter, password storage, IDOR, role checks, state machine). Tests should assert the **specification**, not the current implementation.

Member 4 pins SUT at `85af3ba875c88283615e22cb108f13e2fccaf0e9` when cloning into CI rather than vendoring the whole tree.

### Endpoints behind the allocated features

- FR-01 `POST /api/register`
- FR-02 `POST /api/login`
- FR-04 `GET|PUT /api/users/me`
- FR-05 `GET /api/products?search=`
- FR-07 `GET|POST /api/cart`
- FR-08 `POST /api/checkout`
- FR-09 `POST /api/apply-coupon`
- FR-10 `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` — pending → confirmed → shipping → delivered; cancel from pending/confirmed; `delivered`/`canceled` are terminal; user cannot cancel once `shipping`
- FR-15 `POST|PUT|DELETE /api/products`, `GET /api/products/:id`
- FR-17 `POST /api/admin/coupons`, `DELETE /api/admin/coupons/:id`, `GET /api/coupons`
- FR-18 `GET /api/admin/orders`, `PUT /api/admin/orders/:id/status`
- FR-19 `GET /api/admin/users`, `DELETE /api/admin/users/:id`

Sample coupons: `SAVE10` (10%, min 300k), `BIGBUY` (50k, min 500k), `VIP100` (100k, min 300k, 2 uses), `EXPIRED`.

## Commands

SUT is not on this branch yet. After adding it (clone `ttbhanh/eshop-sut` or copy `eshop-sut/` from `origin/khanh`):

```bash
# Backend (required for all API tests)
cd eshop-sut/backend
npm install
node database.js          # seed / reset SQLite
node server.js            # http://localhost:3000
# or: npm start / npm run start:fresh

# Optional UIs (not needed for Newman)
cd eshop-sut/frontend-web && npm install && npm run dev      # :5173
cd eshop-sut/frontend-admin && npm install && npm run dev    # :5174
```

Newman (install Postman CLI / `npm i -g newman newman-reporter-htmlextra`, or use `npx`):

```bash
# Pattern used on origin/khanh — adapt collection path, env, folder, and newman/member-N/
npx -p newman -p newman-reporter-htmlextra newman run \
  postman/HW06_API_Testing.postman_collection.json \
  -e postman/HW06_Local.postman_environment.json \
  --folder "01_Sanity_Suite" \
  -r htmlextra,cli \
  --reporter-htmlextra-export newman/member-N/ci-report.html
```

Run a single folder/API the same way with `--folder "<folder name>"`. Re-seed the DB immediately before lockout and mutating CRUD suites.

CI: GitHub Actions on teammate branches starts the backend, health-checks `GET /api/products`, then runs Newman. Member 1 splits the collection into `01_Sanity_Suite` (CI green) vs `02_Bug_Discovery_Suite` (expected SUT defects). The assignment also requires a second pipeline run that shows **one intentional failure**.

## Expected layout (create as work lands)

```text
HW06/
├── docs/            # main-report, ai-audit-report, ai-critique, cicd-report, git-commit-log.txt
├── postman/         # collection, environments, data/*.csv
├── newman/member-N/ # HTML (+ JSON) Newman exports
├── test-cases/      # member-N.xlsx (and CSV if generated)
├── bug-reports/     # member-N.md + screenshots / GitHub Issue links
├── agent-skill/     # self-drawn diagram, pseudocode, optional implementation
├── eshop-sut/       # optional vendored SUT
└── README.md        # self-assessment table + test summary counts
```

Reports: Vietnamese for narrative docs; English is fine for Postman scripts and test names. Export Markdown **and** PDF. README must include the 4-row self-assessment rubric (3 APIs × 30 + Agent Skill × 10) and counts: APIs, generated / added / executed / passed / failed, bugs.

Moodle ZIP: `<StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip` with a 3-digit grade `000`–`100`. Missing any required artifact is 0. Late is 0.

## Constraints that must not be faked

TAs verify these; they must not be AI-generated or fabricated:

- `X-Student-Id` header, evidenced by a Postman console screenshot of the pre-request script
- Newman run output whose hostname matches the real deployment
- Agent Skill diagram: **self-drawn** (any tool, but the diagram itself is not AI-generated)

Also required: AI Audit Report (tool, datetime, prompt, output per interaction), 200–300 word AI Critique, commit-per-step log as a text file, CI report with one all-pass run and one failing run (screenshots + links).

Exercise Postman features beyond basic requests (environments, variables, collection/pre-request scripts, data-driven Collection Runner, mock server, etc.) and list them in the report.

When implementing the Agent Skill (G9.5, 10 points): given the API spec, emit test cases. Diagram + pseudocode are mandatory; a reusable skill + YouTube demo is extra credit, not a substitute for the diagram.

## Working conventions from teammates (reuse the pattern, not the APIs)

- Collection-level pre-request: `pm.environment.get('student_id')` → upsert `X-Student-Id`; `console.log` it for the screenshot.
- Dedicated fixture users (lockout, cart, profile) so FR-02 lockout does not poison other suites.
- Sanity folder stays green for CI; put spec-vs-SUT failures in a discovery folder and file them as bugs.
- Commit message shape: `test(member-N): generate|audit|add human|implement Postman` then `docs(member-N): add bug reports`.
- `.gitignore` should exclude `node_modules/`, `*.log`, `server.log`, `*.sqlite-journal`.
