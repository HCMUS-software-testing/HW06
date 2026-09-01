# Test-case catalogue schema

Each row is one independently auditable case. The required fields are:

| Field | Purpose |
|---|---|
| `Test ID` | Stable unique identifier, grouped by feature. |
| `Feature`, `Endpoint`, `Method` | Scope and request target. |
| `Category`, `Requirement/SEC` | Domain/state/security/schema coverage and requirement mapping. |
| `Precondition`, `Test data`, `Steps` | Reproducible setup and execution. |
| `Expected status`, `Expected oracle/schema` | Exact observable result and response contract. |
| `AI source` | Prompt/output batch or `HUMAN`. |
| `Audit label` | `VALID`, `INVALID`, or `INCOMPLETE`. |
| `Audit reason`, `Corrected version`, `Why AI missed` | Human audit trail and extension rationale. |
| `Postman mapping` | Executable collection item/folder. |
| `Execution status`, `Observed status`, `Classification`, `Bug ID`, `Evidence` | Runtime result and defect traceability. |

Before export, validate that every case has an exact expected status, an observable oracle, at least one requirement mapping, and a non-empty audit decision. Validate the per-API count (target >=35) and the human extension count (target >=5).
