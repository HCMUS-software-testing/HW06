# CI/CD Report — Member 4

Workflow: `.github/workflows/hw06-member4.yml`.

## Configuration

GitHub Actions validates secret `STUDENT_ID=23127326`, checks out the submission, clones the SUT at commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`, installs backend dependencies, starts a clean SQLite-backed server, waits for `GET /api/products`, executes Newman and uploads JSON/HTML evidence even when the test step fails.

Push runs use `HW06_member4_ci_demo_collection.json`. It includes stable approved cases representing FR-04, FR-10 and FR-19 plus one explicitly named pipeline-control assertion. With `ci-force-failure.txt=false`, all 22 assertions pass. With `true`, exactly `CI-DEMO-001 controlled assertion` fails; this proves the pipeline detects a red test and is not classified as a SUT defect.

Manual `workflow_dispatch` exposes `conformance`, which runs the full 140-case catalogue. It is intentionally red on the pinned defective SUT (42 failed catalogue cases); hiding those failures to make CI green would falsify the conformance result.

## Recorded runs

All links below are public GitHub Actions runs. Required screenshots must be captured from these actual pages; generated status cards are not accepted.

| Evidence | Commit | Actions run | Expected result | Screenshot |
|---|---|---|---|---|
| CI demo pass | [`90c2b7e`](https://github.com/HCMUS-software-testing/HW06/commit/90c2b7e6ff1cadd24f9d72300de34b646050cdba) | [33498533231](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498533231) | 22/22 assertions pass | `../evidence/github-actions-pass.png` |
| CI demo exact-one-fail | [`10e32d8`](https://github.com/HCMUS-software-testing/HW06/commit/10e32d8) | [33498587297](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498587297) | 21 pass, exactly 1 controlled assertion fail | `../evidence/github-actions-one-fail.png` |
| Restored green branch | [`b0b3764`](https://github.com/HCMUS-software-testing/HW06/commit/b0b3764) | [33498661968](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498661968) | 22/22 assertions pass | same live run page |
| Full conformance | [`b0b3764`](https://github.com/HCMUS-software-testing/HW06/commit/b0b3764) | [33498724665](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498724665) | 467 requests; 839 assertions; 63 product assertions fail | `../evidence/github-actions-full-conformance.png` |
