# CI/CD Report — Member 4

Workflow: `.github/workflows/hw06-member4.yml`.

Pipeline installs Node dependencies in the pinned EShop SUT, initializes SQLite seed data, starts backend on port 3000, waits for `/api/products`, runs Newman, and uploads HTML/JUnit/CLI artifacts. `STUDENT_ID` is supplied through a GitHub Actions secret or repository variable; missing/placeholder values fail fast.

Required evidence:

1. Pass-demo commit: all currently enabled CI checks pass.
2. Fail-demo commit: one assertion labelled `CI-DEMO-FAIL` is intentionally inverted; exactly one test fails.
3. Restore commit: assertion restored; both prior run links/screenshots retained.

The fail-demo is never presented as a product defect. Genuine contract failures remain visible in the conformance run and are linked to bug reports. Add commit hashes, run URLs and screenshots after pushing the branch.

