# CI/CD Report — Member 4

Workflow: `.github/workflows/hw06-member4.yml`.

Pipeline installs Node dependencies in the pinned EShop SUT, initializes SQLite seed data, starts backend on port 3000, waits for `/api/products`, runs a stable green smoke gate, and uploads JSON/CLI artifacts. Full conformance remains available locally through the 150-item collection and is expected to fail on confirmed defects. `STUDENT_ID` is supplied through a GitHub Actions secret; missing/wrong values fail fast.

Required evidence:

1. Pass-demo commit: stable smoke gate passes.
2. Fail-demo commit: full conformance run demonstrates assertion failures from the test suite.
3. Restore commit: assertion restored; both prior run links/screenshots retained.

The fail-demo is never presented as a product defect. Genuine contract failures remain visible in the conformance run and are linked to bug reports. Add commit hashes, run URLs and screenshots after pushing the branch.

## Recorded runs

- Green smoke run: commit [`fd28de2`](https://github.com/HCMUS-software-testing/HW06/commit/fd28de2), Actions run [33414783638](https://github.com/HCMUS-software-testing/HW06/actions/runs/33414783638).
- Full conformance failure: commit [`5cbc0a8`](https://github.com/HCMUS-software-testing/HW06/commit/5cbc0a8), Actions run [33414685928](https://github.com/HCMUS-software-testing/HW06/actions/runs/33414685928); 66 assertions failed, retained for classification.
