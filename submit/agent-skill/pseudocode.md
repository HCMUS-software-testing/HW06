# AI API Test Generator — pseudocode

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

Human gate required before execution: VALID/INVALID/INCOMPLETE label, correction, approved oracle, and evidence mapping.

