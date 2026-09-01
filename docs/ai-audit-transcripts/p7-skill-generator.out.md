AI output (rút gọn)

agent-skill/generate_api_tests.py (~65KB): parse_spec regex `**Endpoint:** METHOD path`; parse_srs phát hiện password policy, email_unique, "lớn hơn hoặc bằng". CSV_FIELDS 17 cột; Case dataclass; folder discovery kèm 00_Setup_Auth. Outputs: test-cases/generated/*.csv, test-cases/member-3.xlsx, postman/HW06_Member3.postman_collection.json.

Ghi chú người (REVISE sau khi chạy thật):
- FR-17-035 Basic auth ban đầu expected 401 → SUT 403 → sửa assertion 403.
- Discovery thiếu 00_Setup_Auth gây 401 hàng loạt → thêm folder setup.
- Lỗi cú pháp `exec_flag := False` trong FR-09-019 → viết lại thành SAVE10 min+1.
