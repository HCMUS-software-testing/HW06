# Pseudocode — AI API Test Generator (Member 3)

Design choices are the student's. This file is the G9.5 pseudocode deliverable.

```
ALGORITHM GenerateApiTests(specPath, srsPath, featureId, studentId, useLlm):

  spec ← PARSE_MARKDOWN_SPEC(specPath)
      // endpoints[], fields[], statusCodes[], authFlags[]
  srs  ← PARSE_SRS_RULES(srsPath, featureId)
      // FR-01: email unique + password policy
      // FR-09: C1..C5, percent/fixed formula, sample coupons
      // FR-17: required fields, admin role, uniqueness

  catalog ← empty list

  // ----- Layer 2: heuristics (always run) -----
  FOR EACH field IN spec.fields:
      catalog ← catalog ∪ EQUIVALENCE_PARTITIONS(field, srs)
      catalog ← catalog ∪ BOUNDARY_VALUES(field, srs)

  catalog ← catalog ∪ DECISION_TABLE(srs.conditions)   // FR-09: 5 coupon rules
  catalog ← catalog ∪ STATE_LIFECYCLE(spec, srs)       // create→use→expire→delete
  catalog ← catalog ∪ SECURITY_MATRIX(SEC-01 .. SEC-07, spec.roles)
  catalog ← catalog ∪ SCHEMA_ASSERTIONS(spec.successShape, spec.errorShape)

  // ----- Layer 3: optional LLM, one technique per call -----
  IF useLlm AND API_KEY_PRESENT:
      FOR EACH technique IN {EP, BVA, DECISION, STATE, SECURITY, SCHEMA}:
          prompt ← BUILD_PROMPT(technique, spec, srs, already=catalog)
          raw    ← LLM_COMPLETE(prompt)          // never "generate everything"
          extra  ← PARSE_CASES(raw)
          catalog ← MERGE_BY_ID(catalog, extra)

  // ----- Human-added slots (engine reserves IDs, student fills) -----
  catalog ← catalog ∪ HUMAN_ADDED_TEMPLATES(featureId)  // ≥ 5, tagged source=HUMAN

  // ----- Layer 4: validate then emit -----
  ASSERT unique(catalog.id)
  ASSERT count(catalog WHERE source=AI) ≥ 35
  ASSERT count(catalog WHERE source=HUMAN) ≥ 5
  ASSERT EVERY case HAS expected_status AND technique AND audit_label

  WRITE CSV  test-cases/generated/{featureId}.csv
  WRITE XLSX test-cases/member-3.xlsx                 // when --all
  WRITE POSTMAN collection:
      pre-request: upsert header X-Student-Id = studentId
      folder 01_Sanity_Suite        // expected == current SUT
      folder 02_Bug_Discovery_Suite // expected == spec, may fail
      folder 03_Data_Driven_Demo
  RETURN catalog
```

## Decision table for FR-09 (engine expands this)

Conditions: C1 exists+active · C2 not expired · C3 total ≥ min_order · C4 authenticated · C5 uses remaining.

| C1 | C2 | C3 | C4 | C5 | Spec result |
| --- | --- | --- | --- | --- | --- |
| T | T | T | T | T | 200, discount per formula |
| F | - | - | - | - | 404 unknown/disabled |
| T | F | T | T | T | 400 expired |
| T | T | F | T | T | 400 below min |
| T | T | T | F | T | 401/403 (SEC-02 / C4) |
| T | T | T | T | F | 400 max uses |

BVA on C3 for `SAVE10` (min = 300000): 299999, 300000, 300001.

Percent formula (spec): `discount = total * discount_value / 100`.
Fixed formula (spec): `discount = discount_value`.
`final_amount = total - discount`.
