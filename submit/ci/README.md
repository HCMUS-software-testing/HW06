# CI full-pass baseline

`sut-conformance-fixes.patch` is applied only to the temporary clone created by the `full-pass` GitHub Actions job. It is not a replacement for the pinned upstream SUT and is not used by the `conformance` job.

Purpose: provide a reproducible regression gate for the audited 140-case collection after correcting the 10 product defects recorded in `bug-reports.md` (credential exposure, profile update validation/partial update, current-user authorization, order cancellation/state transition, admin authorization, delete semantics, stale JWT and malformed JSON handling).

The full-pass job runs `postman/HW06_23127326_collection.json`, not the 3-case demo collection. The verified output is 467 HTTP requests, 839 assertions and 0 assertion failures. The original pinned SUT remains separately testable through `workflow_dispatch → conformance`, where its 42 failing catalogue cases stay visible.
