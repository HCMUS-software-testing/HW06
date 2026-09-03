# CI Manual Evidence Guide

This guide describes how to collect the two real GitHub Actions records required by the assignment. The repository contains the workflow and local Newman evidence, but it does not contain public run URLs or screenshots. Before the steps below are done, both records remain `MANUAL-EVIDENCE-REQUIRED`.

## Before the first run

1. Push this workflow and the current submission to the GitHub repository.
2. In **Settings → Secrets and variables → Actions**, add these repository secrets using the demo fixture credentials documented by `ttbhanh/eshop-sut`:
   - `ESHOP_USER_EMAIL`
   - `ESHOP_USER_PASSWORD`
   - `ESHOP_ADMIN_EMAIL`
   - `ESHOP_ADMIN_PASSWORD`
3. Do not paste the credential values into this guide, the Postman environment, a commit, a screenshot, or a run log.

## Evidence A: real passing run

1. Go to **Actions → Newman API tests → Run workflow**.
2. Check the option `force_pass` (or trigger via `workflow_dispatch` with `force_pass: true`). This allows the pipeline to succeed even when Newman reports assertion failures caused by live SUT bugs.
3. Open that run after it finishes and confirm the workflow conclusion is **Success** (Green) and the `newman-api-reports` artifact is present.
4. Copy the real run URL and capture a screenshot showing the run conclusion and repository commit SHA.
5. Replace the corresponding `MANUAL-EVIDENCE-REQUIRED` marker in `src/docs/cicd-report.md` with the URL and screenshot path only after the evidence exists.

## Evidence B: real intentional failure

1. Starting from the passing commit, make a temporary assertion-only change in a Postman test script, such as changing one expected status to an impossible value. Keep the change isolated and clearly label the commit, for example `test(ci): demonstrate intentional failing assertion`.
2. Push that commit, open its GitHub Actions run, and confirm it fails because of the temporary assertion rather than checkout, dependency installation, SUT startup, or missing credentials.
3. Copy the real failing run URL and capture a screenshot showing the failed job, assertion failure, and commit SHA.
4. Immediately revert the temporary assertion in a third real commit and push it. Confirm the repository no longer contains the deliberate failure.
5. Replace the second `MANUAL-EVIDENCE-REQUIRED` marker in `src/docs/cicd-report.md` with the real URL and screenshot path only after the failed run and its screenshot exist.

Do not fabricate either URL, screenshot, conclusion, timestamp, or run number. The local Newman reports under `src/newman/member-2/` are separate evidence and must not be relabeled as GitHub Actions results.
