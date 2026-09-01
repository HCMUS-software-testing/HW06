# Newman evidence — Member 4

SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`. Host: `http://localhost:3000`. MSSV: `23127326`.

## Full conformance run

- File: `newman-full-report.html` / `.json`
- 142 collection items (2 setup + 140 catalogue)
- 467 HTTP requests including isolated fixtures and postconditions
- 839 assertions: 776 pass, 63 fail
- Catalogue result: 98 PASS, 42 FAIL
- Fixture/request errors: 0
- Classification: 10 unique root product defects

## Data-driven FR-04 phone run

- File: `newman-report.html` / `.json`
- Data: `../../postman/data/fr04-phone-partitions.csv`
- 6 iterations, 12 requests, 18 assertions
- 14 pass, 4 fail; all four failures reproduce invalid phone acceptance (`BUG-04-003`)

The collection-level pre-request script injects and logs `X-Student-Id`. The anti-cheating screenshot must still be captured from the real Postman Console; the machine-readable/HTML reports do not replace that screenshot.
