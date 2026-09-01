# Bộ sinh API test bằng AI — giả mã

```text
function generate_tests(api_spec, requirements, feature):
    contract = normalize_contract(api_spec, feature)
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

    reviewed = human_review_gate(candidates,
        labels=["VALID", "INVALID", "INCOMPLETE"],
        required=["audit_reason", "corrected_version", "oracle"])
    approved = reviewed.filter(label="VALID")
    human_added = add_student_cases(feature, rules,
        focus=["security", "state", "schema", "boundary"])
    approved = critic_review(deduplicate(approved + human_added))

    exports = export(approved, formats=["csv", "xlsx", "postman-ready"])
    results = run_newman_with_fixtures(exports.postman, required_student_header=True)
    defects = classify_root_failures(results)
    return exports, reviewed.audit_log, results, defects
```

Cổng duyệt của người là bắt buộc trước execution: gắn nhãn VALID/INVALID/INCOMPLETE, nêu chỉnh sửa, oracle đã duyệt và ánh xạ minh chứng.
