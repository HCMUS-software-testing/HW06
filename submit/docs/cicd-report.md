# CI/CD Report — Member 4

Workflow: `.github/workflows/hw06-member4.yml`.

## Configuration

GitHub Actions validates secret `STUDENT_ID=23127326`, checks out the submission, clones the SUT at commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`, installs backend dependencies, starts a clean SQLite-backed server, waits for `GET /api/products`, executes Newman and uploads JSON/HTML evidence even when the test step fails.

Push runs use `HW06_member4_ci_demo_collection.json`. It includes stable approved cases representing FR-04, FR-10 and FR-19 plus one explicitly named pipeline-control assertion. With `ci-force-failure.txt=false`, all 22 assertions pass. With `true`, exactly `CI-DEMO-001 controlled assertion` fails; this proves the pipeline detects a red test and is not classified as a SUT defect.

Manual `workflow_dispatch` exposes `conformance`, which runs the full 140-case catalogue. It is intentionally red on the pinned defective SUT (42 failed catalogue cases); hiding those failures to make CI green would falsify the conformance result.

## Recorded runs

The current pass/fail demonstration commit and Actions URLs will be filled after pushing the two controlled commits. Required screenshots must be captured from the actual GitHub Actions pages; generated status cards are not accepted.

| Evidence | Commit | Actions run | Expected result | Screenshot |
|---|---|---|---|---|
| CI demo pass | `PENDING_PUSH` | `PENDING_RUN_URL` | 22/22 assertions pass | `../evidence/github-actions-pass.png` |
| CI demo exact-one-fail | `PENDING_PUSH` | `PENDING_RUN_URL` | 21 pass, exactly 1 controlled assertion fail | `../evidence/github-actions-one-fail.png` |
| Restored green branch | `PENDING_PUSH` | `PENDING_RUN_URL` | 22/22 assertions pass | same live run page |
