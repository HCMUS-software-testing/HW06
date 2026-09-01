---
name: ai-api-test-generator
description: Four-layer Agent Skill that parses the EShop API spec, expands EP/BVA/decision-table/security/schema cases, optionally calls an LLM per technique, validates the set, and emits CSV plus a Postman collection. Demo feature is FR-09.
---

# Agent Skill: AI API Test Generator (G9.5)

Member 3 (Mai Thị Kim Duyên, `23127185`) implement. Input is the SUT spec; output is an auditable test catalog and a runnable Postman collection. The skill does **not** invent Newman HTML or screenshots.

## How to run

```bash
# Demo (FR-09) — assignment G9.5 walkthrough
python agent-skill/generate_api_tests.py \
  --spec eshop-sut/api_specification.md \
  --srs eshop-sut/README.md \
  --feature FR-09 \
  --student-id 23127185

# All three Member 3 APIs + Postman collection + Excel
python agent-skill/generate_api_tests.py --all --student-id 23127185
```

Optional LLM layer (one technique per call). Without an API key the heuristic engine still emits ≥ 35 cases per feature — those cases are the ones produced and audited in this homework session.

```bash
export ANTHROPIC_API_KEY=...   # optional
python agent-skill/generate_api_tests.py --feature FR-09 --use-llm
```

Skill B (audit logger), separate:

```bash
python agent-skill/audit_logger.py \
  --tool "Claude Code (Opus 5)" \
  --task "FR-09 decision table" \
  --prompt-file docs/ai-audit-transcripts/p3-fr09-decision.md \
  --output-file docs/ai-audit-transcripts/p3-fr09-decision.out.md \
  --decision ACCEPT
```

## Four-layer pipeline

1. **Parser** — endpoint, method, body fields, documented status codes, admin-role requirement from `api_specification.md`; coupon rules C1–C5 and password policy from SRS.
2. **Heuristic engine** — equivalence partitions, BVA, decision table, state/lifecycle, SEC-01–SEC-07, response schema. Deterministic. This is the layer that must stay reviewable in an oral defense.
3. **Structured prompting (optional LLM)** — one technique per call, never “generate all 35 cases”. Output is merged, not trusted blindly.
4. **Validator** — unique IDs `M3-<FR>-<nnn>`, ≥ 35 cases, every case has expected status + technique tag, human-added cases ≥ 5. Then emit CSV / XLSX / Postman.

See `diagram.svg` (geometry composed by the student; not an image-model render) and `pseudocode.md`.

## Design decisions (why this, not a chat dump)

- Spec is the oracle. Generated expected values follow SRS/API spec, not the current SUT. That is why the collection splits `01_Sanity_Suite` (behaviour the SUT already satisfies) from `02_Bug_Discovery_Suite` (spec assertions that fail on purpose).
- FR-09 is the demo feature because C1–C5 is a real decision table; it is the easiest place to show the engine is not a one-shot prompt.
- The generator never writes Newman HTML. Execution is a separate step (`npx newman ...`) so anti-cheat evidence stays real.
- Student id is injected only via Postman collection pre-request (`X-Student-Id`), never hard-coded per request.

## Outputs

| File | Produced by |
| --- | --- |
| `test-cases/generated/FR-0{1,9,17}.csv` | Layer 4 |
| `test-cases/member-3.xlsx` | Layer 4 (`--all`) |
| `postman/HW06_Member3.postman_collection.json` | Layer 4 (`--all`) |
