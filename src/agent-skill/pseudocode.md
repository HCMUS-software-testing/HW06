# AI-Driven API Test Generator - Pseudocode & Design

**Tác giả:** Lê Trung Kiên (MSSV: 23127075)  

## 1. Thiết Kế Hệ Thống
Hệ thống là một Agent Skill tự động sinh test cases API dựa trên đặc tả đầu vào (`api_specification.md` hoặc OpenAPI YAML/JSON), chia thành 4 giai đoạn sinh thử nghiệm chuyên biệt:
1. **Phân hoạch miền (Domain Partitioning)**
2. **Máy trạng thái (State Transition)**
3. **Bảo mật (Security & RBAC)**
4. **Kiểm tra Schema (Response Schema Validation)**

---

## 2. Pseudocode

```python
function generate_api_test_suite(api_spec_file, target_endpoint):
    spec = parse_api_specification(api_spec_file)
    endpoint_info = spec.get_endpoint(target_endpoint)
    
    test_cases = []
    
    # Step 1: Domain Partitioning Tests (Partition inputs into valid/invalid/boundary)
    domain_tests = ai_prompt_generate(
        template="domain_partitioning",
        params=endpoint_info.parameters,
        target_count=15
    )
    test_cases.extend(domain_tests)
    
    # Step 2: State Transition Tests (For stateful APIs like Checkout & Order status)
    if endpoint_info.is_stateful:
        state_tests = ai_prompt_generate(
            template="state_machine",
            states=endpoint_info.possible_states,
            rules=endpoint_info.transition_rules,
            target_count=10
        )
        test_cases.extend(state_tests)
        
    # Step 3: Security & Authorization Tests (SEC-01 to SEC-07, SQLi, IDOR, RBAC)
    security_tests = ai_prompt_generate(
        template="security_sec01_sec07",
        security_requirements=spec.security_requirements,
        target_count=10
    )
    test_cases.extend(security_tests)
    
    # Step 4: Schema Validation Tests
    schema_tests = ai_prompt_generate(
        template="response_schema",
        expected_schema=endpoint_info.response_schema,
        target_count=5
    )
    test_cases.extend(schema_tests)
    
    # Step 5: Self-Audit & Deduplication
    audited_suite = auto_audit_and_deduplicate(test_cases)
    
    return export_to_postman_collection(audited_suite)
```
