# HW06 Team Task Allocation

## Purpose

This document divides HW06 work for a 4-member team while preserving the assignment constraint: each member owns three selected APIs, including one API from Pool A, one API from Pool B, and one API from Pool C. No two members should use the same three-API selection.

The original homework is written as an individual assignment. Use this plan to coordinate work, avoid duplicated API choices, standardize evidence, and share infrastructure. Each member should still keep their own AI audit, test cases, execution evidence, bug reports, and commit log for the APIs they own.

## Recommended API Ownership

| Member | Pool A API | Pool B API | Pool C API | Why This Assignment Fits |
| --- | --- | --- | --- | --- |
| Member 1 | FR-02: Login and account lockout | FR-07: Shopping cart | FR-15: Product management CRUD | Good mix of authentication, user-side stateful data, and admin CRUD validation. |
| Member 2 | FR-05: Product listing and search | FR-08: Checkout / order creation | FR-18: Order management admin | Strong coverage of query parameters, order creation, and order state changes. |
| Member 3 | FR-01: Account registration | FR-09: Discount coupons | FR-17: Coupon management CRUD | Keeps coupon user/admin behavior together and covers domain validation heavily. |
| Member 4 | FR-04: Personal profile management | FR-10: Order state machine | FR-19: User management admin | Focuses on identity data, state transitions, and access-control sensitive admin APIs. |

## Per-Member Required Pipeline

Each member repeats this pipeline for each of their three APIs.

| Step | Required Work | Output Evidence |
| --- | --- | --- |
| 1 | Read the relevant part of `api_specification.md`, including request parameters, response schema, roles, and SEC-01 to SEC-07 requirements. | Notes in the member report section. |
| 2 | Use AI step by step to generate test cases, targeting at least 35 test cases per API. | AI prompts and outputs in AI Audit Report. |
| 3 | Audit every AI-generated test case as `VALID`, `INVALID`, or `INCOMPLETE`, with reasoning. | Audited test case table. |
| 4 | Correct invalid and incomplete AI-generated test cases. | Final corrected test case table. |
| 5 | Add at least 5 human-written test cases that AI missed, especially security and state-transition cases. | Added test case table plus explanation of why AI missed them. |
| 6 | Implement the final test cases in Postman. | Postman collection requests and test scripts. |
| 7 | Ensure every request sends `X-Student-Id: {StudentID}`. | Console screenshot from pre-request script. |
| 8 | Execute with Newman and export the HTML report. | Newman terminal output and HTML report. |
| 9 | Report real bugs in Markdown and GitHub Issues, with screenshots. | Bug report section and GitHub Issue links. |
| 10 | Commit after major steps: generation, audit, extension, execution, and bug reporting. | Git commit log text file. |

## Shared Team Responsibilities

| Area | Primary Owner | Supporting Members | Deliverables |
| --- | --- | --- | --- |
| SUT setup | Member 1 | All | Local setup notes, seed data notes, confirmed base URL. |
| Postman standards | Member 1 | All | Shared workspace structure, environment variables, `X-Student-Id` pre-request script pattern. |
| Test case template | Member 2 | All | Common Excel columns, naming convention, expected result format. |
| CI/CD pipeline | Member 2 | Member 1 | GitHub Actions workflow running Newman, one passing run, one intentionally failing run. |
| Report integration | Member 3 | All | Main Markdown report structure, merged test summary, consistent screenshots and links. |
| AI Audit format | Member 3 | All | Standard audit log format: AI tool, date/time, prompt, output, human decision. |
| Agent Skill design | Member 4 | All | Self-drawn diagram, pseudocode, optional reusable Agent Skill implementation, optional demo video. |
| Final packaging | Member 4 | All | ZIP checklist, README self-assessment table, final file naming check. |

## Suggested Folder Structure

Use this structure so each member's evidence remains separate and easy to review.

```text
HW06/
├── docs/
│   ├── hw06-team-task-allocation.md
│   ├── main-report.md
│   ├── ai-audit-report.md
│   ├── ai-critique.md
│   ├── cicd-report.md
│   └── git-commit-log.txt
├── postman/
│   ├── HW06_API_Testing.postman_collection.json
│   ├── HW06_Local.postman_environment.json
│   └── data/
├── newman/
│   ├── member-1/
│   ├── member-2/
│   ├── member-3/
│   └── member-4/
├── test-cases/
│   ├── member-1.xlsx
│   ├── member-2.xlsx
│   ├── member-3.xlsx
│   └── member-4.xlsx
├── bug-reports/
│   ├── member-1.md
│   ├── member-2.md
│   ├── member-3.md
│   └── member-4.md
└── agent-skill/
    ├── diagram.png
    ├── pseudocode.md
    └── skill-demo-notes.md
```

## API-Specific Test Focus

| Member | API | Main Coverage Focus |
| --- | --- | --- |
| Member 1 | FR-02 Login and account lockout | Valid login, invalid credentials, lockout threshold, locked account behavior, token response schema, SQL injection, brute-force resistance. |
| Member 1 | FR-07 Shopping cart | Add item, update quantity, remove item, invalid product ID, quantity boundaries, unauthenticated access, IDOR on cart ownership. |
| Member 1 | FR-15 Product management CRUD | Admin authorization, create/update/delete product, invalid price and stock, missing fields, schema validation, role escalation checks. |
| Member 2 | FR-05 Product listing and search | Query partitions, pagination, sorting, keyword edge cases, invalid filters, response schema, injection in query parameters. |
| Member 2 | FR-08 Checkout / order creation | Valid checkout, empty cart, insufficient stock, invalid address, coupon interaction, unauthenticated checkout, schema validation. |
| Member 2 | FR-18 Order management admin | Admin-only access, order status update, invalid transitions, unauthorized user access, IDOR, response schema. |
| Member 3 | FR-01 Account registration | Email format partitions, password complexity, duplicate account, missing fields, long input, SQL injection, response schema. |
| Member 3 | FR-09 Discount coupons | Valid coupon, expired coupon, usage limit, minimum order value, invalid code, repeated use, coupon ownership or role checks. |
| Member 3 | FR-17 Coupon management CRUD | Admin authorization, create/update/delete coupon, invalid date range, invalid discount value, duplicate code, role escalation. |
| Member 4 | FR-04 Personal profile management | View/update profile, invalid phone/email/name, unauthorized access, IDOR on another profile, schema validation. |
| Member 4 | FR-10 Order state machine | Pending to confirmed to shipping to delivered, cancellation rules, invalid backward transitions, repeated transitions, unauthorized transition. |
| Member 4 | FR-19 User management admin | Admin-only user listing/update, role changes, self-demotion edge case, IDOR, blocked user handling, schema validation. |

## Minimum Workload Per Member

| Metric | Minimum Per API | Minimum Per Member |
| --- | ---: | ---: |
| AI-generated test cases | 35 | 105 |
| Human-added test cases | 5 | 15 |
| Audited test cases | 35 | 105 |
| APIs executed with Newman | 1 | 3 |
| GitHub bug issues | Report all genuine bugs found | Report all genuine bugs found |
| Major commits | At least 4 per API | At least 12 |

## Commit Plan

Each member should use clear commit messages. Recommended sequence:

```text
test(member-1): generate API test cases for FR-02 FR-07 FR-15
test(member-1): audit generated API test cases
test(member-1): add human-designed API test cases
test(member-1): implement Postman tests and Newman reports
docs(member-1): add bug reports and evidence links
```

Repeat the same pattern for `member-2`, `member-3`, and `member-4`.

## Final Integration Checklist

- [ ] All four members have three APIs selected, one from Pool A, one from Pool B, and one from Pool C.
- [ ] No two members use the same three-API combination.
- [ ] Every selected API has at least 35 AI-generated test cases.
- [ ] Every selected API has all AI-generated cases audited as `VALID`, `INVALID`, or `INCOMPLETE`.
- [ ] Every selected API has at least 5 human-added test cases.
- [ ] Every request includes `X-Student-Id: {StudentID}`.
- [ ] Newman HTML reports are exported and linked.
- [ ] Postman features used are listed in the report.
- [ ] CI/CD has one passing pipeline run and one intentionally failing pipeline run.
- [ ] Real bugs are reported both in Markdown and GitHub Issues with screenshots.
- [ ] AI Audit Report includes tool name, date/time, prompt, and AI output for each interaction.
- [ ] AI Critique is 200-300 words.
- [ ] Agent Skill design includes a self-drawn diagram and pseudocode.
- [ ] Git commit log is exported as a text file.
- [ ] README includes the self-assessment table and test summary.
- [ ] Final ZIP follows `<StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip`.

## Practical Execution Order

1. Agree on the API ownership table before writing tests.
2. Set up the SUT and shared Postman environment.
3. Each member generates and audits test cases for their three APIs.
4. Each member implements Postman tests and exports Newman evidence.
5. The team integrates the collection into CI/CD.
6. Each member finishes bug reports, AI audit, and test summary.
7. The team merges report sections and checks the final ZIP checklist.
