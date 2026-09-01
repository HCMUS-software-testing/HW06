# HW06 - Phân Công Công Việc Nhóm

## Mục Đích

Tài liệu này chia công việc HW06 cho nhóm 4 thành viên, đồng thời vẫn giữ đúng ràng buộc của đề: mỗi thành viên sở hữu ba API được chọn, gồm một API từ Pool A, một API từ Pool B, và một API từ Pool C. Không hai thành viên nào nên dùng cùng một bộ ba API.

Đề gốc được viết theo dạng bài tập cá nhân. Vì vậy, hãy dùng kế hoạch này để phối hợp công việc, tránh chọn trùng API, chuẩn hóa bằng chứng, và chia sẻ phần hạ tầng chung. Mỗi thành viên vẫn nên giữ riêng AI audit, test cases, bằng chứng thực thi, bug reports, và commit log cho các API mình phụ trách.

## Phân Công API Đề Xuất

| Thành viên | API Pool A | API Pool B | API Pool C | Lý do phân công phù hợp |
| --- | --- | --- | --- | --- |
| Thành viên 1 | FR-02: Đăng nhập và khóa tài khoản | FR-07: Giỏ hàng | FR-15: Quản lý sản phẩm CRUD | Cân bằng giữa xác thực, dữ liệu trạng thái phía người dùng, và kiểm tra CRUD phía admin. |
| Thành viên 2 (Lê Trung Kiên - 23127075) | FR-05: Liệt kê và tìm kiếm sản phẩm | FR-08: Thanh toán / tạo đơn hàng | FR-18: Quản lý đơn hàng admin | Bao phủ tốt query parameters, tạo đơn hàng, và thay đổi trạng thái đơn hàng. |
| Thành viên 3 | FR-01: Đăng ký tài khoản | FR-09: Mã giảm giá | FR-17: Quản lý mã giảm giá CRUD | Gom hành vi coupon phía người dùng và admin lại với nhau, đồng thời có nhiều kiểm thử phân hoạch miền. |
| Thành viên 4 | FR-04: Quản lý hồ sơ cá nhân | FR-10: Máy trạng thái đơn hàng | FR-19: Quản lý người dùng admin | Tập trung vào dữ liệu định danh, chuyển trạng thái, và các API admin nhạy cảm về phân quyền. |

## Pipeline Bắt Buộc Cho Mỗi Thành Viên

Mỗi thành viên lặp lại pipeline này cho từng API trong ba API mình phụ trách.

| Bước | Công việc bắt buộc | Bằng chứng đầu ra |
| --- | --- | --- |
| 1 | Đọc phần liên quan trong `api_specification.md`, gồm request parameters, response schema, roles, và các yêu cầu SEC-01 đến SEC-07. | Ghi chú trong phần báo cáo của thành viên. |
| 2 | Dùng AI từng bước để sinh test cases, mục tiêu ít nhất 35 test cases cho mỗi API. | Prompts và outputs trong AI Audit Report. |
| 3 | Kiểm toán từng test case do AI sinh ra với nhãn `VALID`, `INVALID`, hoặc `INCOMPLETE`, kèm lý do. | Bảng test cases đã audit. |
| 4 | Sửa các test cases không hợp lệ hoặc chưa hoàn chỉnh. | Bảng test cases cuối cùng đã chỉnh sửa. |
| 5 | Tự thêm ít nhất 5 test cases mà AI bỏ sót, đặc biệt là các case về bảo mật và chuyển trạng thái. | Bảng test cases tự thêm và giải thích vì sao AI bỏ sót. |
| 6 | Implement bộ test cases cuối cùng trong Postman. | Các requests và test scripts trong Postman collection. |
| 7 | Đảm bảo mọi request gửi header `X-Student-Id: {StudentID}`. | Ảnh chụp console từ pre-request script. |
| 8 | Chạy bằng Newman và export HTML report. | Newman terminal output và HTML report. |
| 9 | Báo cáo bug thật trong Markdown và GitHub Issues, kèm screenshots. | Phần bug report và link GitHub Issues. |
| 10 | Commit sau các bước chính: generation, audit, extension, execution, và bug reporting. | File text Git commit log. |

## Trách Nhiệm Chung Của Nhóm

| Hạng mục | Người phụ trách chính | Thành viên hỗ trợ | Deliverables |
| --- | --- | --- | --- |
| Setup SUT | Thành viên 1 | Tất cả | Ghi chú setup local, ghi chú seed data, base URL đã xác nhận. |
| Chuẩn Postman | Thành viên 1 | Tất cả | Cấu trúc workspace chung, environment variables, mẫu pre-request script cho `X-Student-Id`. |
| Template test case | Thành viên 2 (Lê Trung Kiên - 23127075) | Tất cả | Các cột Excel thống nhất, quy ước đặt tên, format expected result. |
| Pipeline CI/CD | Thành viên 2 (Lê Trung Kiên - 23127075) | Thành viên 1 | GitHub Actions workflow chạy Newman, một run pass toàn bộ, một run fail có chủ đích. |
| Tích hợp báo cáo | Thành viên 3 | Tất cả | Cấu trúc main Markdown report, test summary đã gộp, screenshots và links thống nhất. |
| Format AI Audit | Thành viên 3 | Tất cả | Format audit log chuẩn: công cụ AI, ngày/giờ, prompt, output, quyết định của con người. |
| Thiết kế Agent Skill | Thành viên 4 | Tất cả | Sơ đồ tự vẽ, pseudocode, tùy chọn implement Agent Skill reusable, tùy chọn demo video. |
| Đóng gói cuối | Thành viên 4 | Tất cả | ZIP checklist, bảng self-assessment trong README, kiểm tra tên file cuối. |

## Cấu Trúc Thư Mục Đề Xuất

Dùng cấu trúc này để bằng chứng của từng thành viên tách biệt và dễ kiểm tra.

```text
HW06/
├── docs/
│   ├── hw06-team-task-allocation.md
│   ├── hw06-phan-cong-cong-viec-nhom.md
│   ├── main-report.md
│   ├── ai-audit-report.md
│   ├── ai-critique.md
│   ├── cicd-report.md
│   └── git-commit-log.txt
├── postman/
│   ├── HW06_API_Testing.postman_collection.json
│   ├── HW06_Local.postman_environment.json
│   └── data/
├── newman/
│   ├── member-1/
│   ├── member-2/
│   ├── member-3/
│   └── member-4/
├── test-cases/
│   ├── member-1.xlsx
│   ├── member-2.xlsx
│   ├── member-3.xlsx
│   └── member-4.xlsx
├── bug-reports/
│   ├── member-1.md
│   ├── member-2.md
│   ├── member-3.md
│   └── member-4.md
└── agent-skill/
    ├── diagram.png
    ├── pseudocode.md
    └── skill-demo-notes.md
```

## Trọng Tâm Kiểm Thử Theo API

| Thành viên | API | Trọng tâm bao phủ chính |
| --- | --- | --- |
| Thành viên 1 | FR-02 Đăng nhập và khóa tài khoản | Đăng nhập hợp lệ, sai credentials, ngưỡng lockout, hành vi tài khoản bị khóa, schema response token, SQL injection, chống brute force. |
| Thành viên 1 | FR-07 Giỏ hàng | Thêm sản phẩm, cập nhật số lượng, xóa sản phẩm, product ID không hợp lệ, biên số lượng, truy cập chưa xác thực, IDOR trên quyền sở hữu giỏ hàng. |
| Thành viên 1 | FR-15 Quản lý sản phẩm CRUD | Phân quyền admin, tạo/cập nhật/xóa sản phẩm, giá và tồn kho không hợp lệ, thiếu trường, schema validation, kiểm tra leo thang vai trò. |
| Thành viên 2 (Lê Trung Kiên - 23127075) | FR-05 Liệt kê và tìm kiếm sản phẩm | Phân hoạch query, phân trang, sắp xếp, keyword edge cases, filter không hợp lệ, response schema, injection trong query parameters. |
| Thành viên 2 (Lê Trung Kiên - 23127075) | FR-08 Thanh toán / tạo đơn hàng | Checkout hợp lệ, giỏ hàng rỗng, thiếu tồn kho, địa chỉ không hợp lệ, tương tác coupon, checkout chưa xác thực, schema validation. |
| Thành viên 2 (Lê Trung Kiên - 23127075) | FR-18 Quản lý đơn hàng admin | Chỉ admin được truy cập, cập nhật trạng thái đơn hàng, chuyển trạng thái không hợp lệ, user không có quyền, IDOR, response schema. |
| Thành viên 3 | FR-01 Đăng ký tài khoản | Phân hoạch định dạng email, độ phức tạp mật khẩu, tài khoản trùng, thiếu trường, input quá dài, SQL injection, response schema. |
| Thành viên 3 | FR-09 Mã giảm giá | Coupon hợp lệ, coupon hết hạn, giới hạn lượt dùng, giá trị đơn hàng tối thiểu, mã không hợp lệ, dùng lặp lại, kiểm tra ownership hoặc role. |
| Thành viên 3 | FR-17 Quản lý mã giảm giá CRUD | Phân quyền admin, tạo/cập nhật/xóa coupon, khoảng ngày không hợp lệ, giá trị giảm không hợp lệ, mã trùng, leo thang vai trò. |
| Thành viên 4 | FR-04 Quản lý hồ sơ cá nhân | Xem/cập nhật hồ sơ, phone/email/name không hợp lệ, truy cập chưa xác thực, IDOR vào hồ sơ người khác, schema validation. |
| Thành viên 4 | FR-10 Máy trạng thái đơn hàng | Pending -> confirmed -> shipping -> delivered, quy tắc hủy, chuyển ngược không hợp lệ, chuyển trạng thái lặp, chuyển trạng thái không có quyền. |
| Thành viên 4 | FR-19 Quản lý người dùng admin | Chỉ admin được list/update user, thay đổi role, edge case tự hạ quyền, IDOR, xử lý user bị khóa, schema validation. |

## Khối Lượng Tối Thiểu Mỗi Thành Viên

| Chỉ số | Tối thiểu mỗi API | Tối thiểu mỗi thành viên |
| --- | ---: | ---: |
| Test cases do AI sinh | 35 | 105 |
| Test cases tự thêm | 5 | 15 |
| Test cases được audit | 35 | 105 |
| API được chạy bằng Newman | 1 | 3 |
| GitHub bug issues | Báo cáo toàn bộ bug thật tìm được | Báo cáo toàn bộ bug thật tìm được |
| Commit chính | Ít nhất 4 mỗi API | Ít nhất 12 |

## Kế Hoạch Commit

Mỗi thành viên nên dùng commit message rõ ràng. Trình tự đề xuất:

```text
test(member-1): generate API test cases for FR-02 FR-07 FR-15
test(member-1): audit generated API test cases
test(member-1): add human-designed API test cases
test(member-1): implement Postman tests and Newman reports
docs(member-1): add bug reports and evidence links
```

Lặp lại cùng pattern cho `member-2`, `member-3`, và `member-4`.

## Checklist Tích Hợp Cuối

- [ ] Cả bốn thành viên đều có ba API được chọn, gồm một API từ Pool A, một API từ Pool B, và một API từ Pool C.
- [ ] Không hai thành viên nào dùng cùng một bộ ba API.
- [ ] Mỗi API được chọn có ít nhất 35 test cases do AI sinh.
- [ ] Mỗi API được chọn có toàn bộ test cases do AI sinh được audit bằng nhãn `VALID`, `INVALID`, hoặc `INCOMPLETE`.
- [ ] Mỗi API được chọn có ít nhất 5 test cases tự thêm.
- [ ] Mọi request đều có header `X-Student-Id: {StudentID}`.
- [ ] Newman HTML reports đã được export và liên kết trong báo cáo.
- [ ] Các tính năng Postman đã dùng được liệt kê trong báo cáo.
- [ ] CI/CD có một pipeline run pass toàn bộ và một pipeline run fail có chủ đích.
- [ ] Bug thật được báo cáo trong cả Markdown và GitHub Issues, kèm screenshots.
- [ ] AI Audit Report có tên công cụ, ngày/giờ, prompt, và output AI cho mỗi lần tương tác.
- [ ] AI Critique dài 200-300 từ.
- [ ] Thiết kế Agent Skill có sơ đồ tự vẽ và pseudocode.
- [ ] Git commit log được export thành file text.
- [ ] README có bảng self-assessment và test summary.
- [ ] File ZIP cuối tuân theo format `<StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip`.

## Thứ Tự Thực Hiện Thực Tế

1. Thống nhất bảng phân công API trước khi viết test.
2. Setup SUT và shared Postman environment.
3. Mỗi thành viên sinh và audit test cases cho ba API của mình.
4. Mỗi thành viên implement Postman tests và export Newman evidence.
5. Nhóm tích hợp collection vào CI/CD.
6. Mỗi thành viên hoàn thiện bug reports, AI audit, và test summary.
7. Nhóm gộp các phần báo cáo và kiểm tra checklist ZIP cuối.
