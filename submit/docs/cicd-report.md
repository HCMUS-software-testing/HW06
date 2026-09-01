# CI/CD Report — Member 4

Workflow: `.github/workflows/hw06-member4.yml`.

Pipeline installs Node dependencies in the pinned EShop SUT, initializes SQLite seed data, starts backend on port 3000, waits for `/api/products`, runs a stable green smoke gate, and uploads JSON/CLI artifacts. Full conformance remains available locally through the 150-item collection and is expected to fail on confirmed defects. `STUDENT_ID` is supplied through a GitHub Actions secret; missing/wrong values fail fast.

Required evidence:

1. Pass-demo commit: stable smoke gate passes.
2. Fail-demo commit: full conformance run demonstrates assertion failures from the test suite.
3. Restore commit: assertion restored; both prior run links/screenshots retained.

The fail-demo is never presented as a product defect. Genuine contract failures remain visible in the conformance run and are linked to bug reports. Screenshots are stored in `../evidence/` and the run metadata is linked below.

## Recorded runs

- Green smoke run: commit [`a910c56`](https://github.com/HCMUS-software-testing/HW06/commit/a910c56), Actions run [33415727552](https://github.com/HCMUS-software-testing/HW06/actions/runs/33415727552); Student ID validation and all 7 selected smoke assertions passed. Screenshot: `../evidence/CI-pass-run-33415727552.png`.
- Full conformance failure: Actions run [33414685928](https://github.com/HCMUS-software-testing/HW06/actions/runs/33414685928); Newman executed the 150-item collection and failed on the recorded 66 assertions. Screenshot: `../evidence/CI-fail-run-33414685928.png`.
- Restored branch: subsequent pushes [`127c6a4`](https://github.com/HCMUS-software-testing/HW06/commit/127c6a4) and [`a910c56`](https://github.com/HCMUS-software-testing/HW06/commit/a910c56) retain the workflow and evidence links.

The green job is intentionally a stable smoke gate; the full 150-item conformance run remains a separate diagnostic run because the pinned SUT reproduces four confirmed defects and 62 fixture issues.
