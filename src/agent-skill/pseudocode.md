# AI-Driven API Test Generator - Pseudocode & Design

**Tác giả:** Lê Trung Kiên (MSSV: 23127075)

## 1. Thiết kế

Skill sinh candidate test từ hợp đồng API/FR/SEC, rồi **dừng** cho người review. Case chỉ thành final/executable sau nhãn người `VALID`, `INVALID`, hoặc `INCOMPLETE` và quyết định correction/exclusion.

Luồng dữ liệu:

1. Parse contracts → endpoint map, schemas, RBAC, state machine.
2. Generate partitions: domain, schema, state paths, authorization abuse.
3. Deduplicate by semantic signature.
4. Human review gate (bắt buộc).
5. Export traceability + Postman/Newman IDs.
6. Ingest execution results; không tự đổi oracle vì fail.

`diagram.mermaid` là sơ đồ do sinh viên tự vẽ; skill không regenerate file đó.

## 2. Pseudocode

```python
function parse_contracts(api_spec, fr_spec, sec_spec):
    endpoints = parse_openapi_or_markdown(api_spec)
    requirements = parse_fr_sec(fr_spec, sec_spec)
    return ContractBundle(endpoints, requirements)

function domain_partitions(endpoint):
    return valid_invalid_boundary_cases(endpoint.parameters, endpoint.body)

function schema_assertions(endpoint):
    return type_presence_media_type_cases(endpoint.success_schema, endpoint.error_schema)

function state_machine_paths(endpoint):
    if not endpoint.state_model:
        return []
    return happy_paths(endpoint.state_model) + illegal_transitions(endpoint.state_model)

function authorization_abuse_cases(endpoint, security):
    return [
        missing_token(endpoint),
        invalid_token(endpoint),
        wrong_role(endpoint, security.rbac),
        idor_cross_user(endpoint),
        mass_assignment(endpoint, security.forbidden_fields),
    ]

function semantic_signature(case):
    return (case.method, normalize_route(case.route), case.auth_mode,
            canonicalize(case.payload), canonicalize(case.oracle))

function deduplicate(cases):
    unique = {}
    for case in cases:
        unique.setdefault(semantic_signature(case), case)
    return list(unique.values())

function human_review(candidates):
    reviewed = []
    for case in candidates:
        verdict = wait_for_human(case)  # VALID | INVALID | INCOMPLETE
        if verdict == "VALID":
            reviewed.append(finalize(case))
        elif verdict == "INVALID":
            replacement = wait_for_human_correction_or_exclude(case)
            if replacement and replacement.approved:
                reviewed.append(finalize(replacement))
            else:
                reviewed.append(exclude(case, reason=replacement.reason))
        else:  # INCOMPLETE
            completed = wait_for_human_to_fill_oracle(case)
            if completed.approved:
                reviewed.append(finalize(completed))
            else:
                reviewed.append(exclude(case, reason="incomplete-unresolved"))
    return reviewed

function export_traceability(final_cases):
    rows = []
    for case in final_cases:
        rows.append({
            "id": case.id,
            "class": case.execution_class,  # NEWMAN | BROWSER-MANUAL | FAULT-INJECTION | EXCLUDED
            "assertion_id": case.id if case.execution_class == "NEWMAN" else None,
            "target": newman_report_path(case) if case.execution_class == "NEWMAN" else "NOT-RUN",
        })
    return rows

function ingest_execution(summary_json, traceability):
    # Map assertion pass/fail onto NEWMAN rows only.
    # Never promote EXCLUDED/manual rows into executed counts.
    return join(summary_json.assertions, traceability.newman_rows)

function generate_api_test_suite(api_spec, fr_spec, sec_spec, target_endpoint):
    contracts = parse_contracts(api_spec, fr_spec, sec_spec)
    endpoint = contracts.endpoints.get(target_endpoint)
    candidates = []
    candidates += domain_partitions(endpoint)
    candidates += schema_assertions(endpoint)
    candidates += state_machine_paths(endpoint)
    candidates += authorization_abuse_cases(endpoint, contracts.requirements.security)
    candidates = deduplicate(candidates)
    # HARD GATE: no candidate is final or executable yet.
    final_cases = human_review(candidates)
    traceability = export_traceability(final_cases)
    return Suite(final_cases, traceability)
```

## 3. Ràng buộc review

- Generator không ghi Postman assertion cho case chưa `approved`.
- INVALID duplicate phải EXCLUDED, không chạy NEWMAN lần hai.
- Execution ingestion chỉ đếm assertion Newman; README/Excel phải lấy số từ `summary.json`.
