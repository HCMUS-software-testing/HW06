# Bộ sinh API test bằng AI — giả mã

```text
function generate_tests(api_spec, requirements, feature):
    contract = parse_endpoints(api_spec, feature)
    rules = select_requirements(requirements, feature)
    assert contract is not empty

    partitions = design_input_partitions(contract, rules)
    states = design_state_graph(contract, rules)
    security = map_security_cases(contract, rules.SEC_01_to_SEC_07)
    schemas = derive_response_invariants(contract, rules)

    candidates = []
    candidates += draft_cases("domain", partitions)
    candidates += draft_cases("state", states)
    candidates += draft_cases("security", security)
    candidates += draft_cases("schema", schemas)

    candidates = assign_stable_ids(candidates, prefix=feature)
    candidates = deduplicate_by_endpoint_input_oracle(candidates)
    candidates = attach_traceability(candidates, contract, rules)
    candidates = attach_setup_data_cleanup(candidates)
    candidates = critic_review(candidates)

    return export(candidates, formats=["csv", "xlsx", "postman-ready"]),
           human_review_queue(candidates)
```

Cổng duyệt của người là bắt buộc trước execution: gắn nhãn VALID/INVALID/INCOMPLETE, nêu chỉnh sửa, oracle đã duyệt và ánh xạ minh chứng.
