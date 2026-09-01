# Báo cáo kiểm toán AI — MSSV 23127326

## Khai báo

Tôi sử dụng công cụ AI cho các công việc: trích xuất yêu cầu, phân tích contract và rủi ro, soạn test case, hỗ trợ audit từng dòng, triển khai fixture/Postman/CI, đối soát kết quả và cấu trúc tài liệu. Sinh viên chịu trách nhiệm về oracle cuối, bản sửa, thực thi và quyết định lỗi.

## Nhật ký tương tác

Thời gian AI-001–AI-005 được giữ từ commit ghi nhận output lần đầu. Output có cấu trúc đầy đủ nằm trong `test-cases/23127326.json`; phần tóm tắt này không thay thế output đó.

### AI-001 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** Trích xuất contract endpoint FR-04, FR-10 và FR-19 từ `api_specification.md` và SRS chuẩn tắc. Liệt kê actor, input, output, role, đồ thị trạng thái và quy tắc SEC liên quan. Đánh dấu giả định schema/status chưa được quy định.

**Output của AI:** Danh mục chuẩn hóa cho `GET/PUT /api/users/me`, endpoint trạng thái đơn của Admin/User và endpoint liệt kê/xóa user; actor, giả định status và ánh xạ SEC-01–SEC-07. AI chỉ ra SEC-07 thuộc FR-03 và FR-19 không có endpoint cập nhật role.

**Quyết định của sinh viên:** Chấp nhận danh mục endpoint; ghi rõ SEC-07 là N/A và không cho phép bịa endpoint.

### AI-002 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** Với FR-04, tạo ít nhất 40 API test case khác nhau. Phân hoạch phone/name/address; bao phủ xác thực, identity binding, mass assignment, trường nhạy cảm, output an toàn XSS và response schema chính xác. Gồm precondition, data, kết quả mong đợi, cleanup và traceability.

**Output của AI:** 40 dòng ứng viên FR-04 có cấu trúc, bao phủ xác thực, biên miền, schema, trường nhạy cảm và bảo mật. ID và bản sửa cuối là `FR04-001`–`FR04-040` trong catalogue JSON.

**Quyết định của sinh viên:** Viết lại fixture chung và status thay thế thành setup cô lập, một status nguyên chính xác và postcondition; giữ 40 case là VALID sau khi sửa.

### AI-003 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** Với FR-10, tạo ma trận chuyển trạng thái 5×5 đầy đủ, cùng case hủy, ownership, role, replay, status sai, terminal state và schema. Không bịa endpoint.

**Output của AI:** 45 dòng ứng viên FR-10 chứa mọi cặp source/destination và biến thể bảo mật/schema (`FR10-001`–`FR10-045`).

**Quyết định của sinh viên:** Gắn mỗi transition với fixture order riêng, xác minh đồ thị trạng thái chuẩn tắc và thêm GET postcondition trước khi gán VALID.

### AI-004 — Codex — 2026-08-31 23:31:15 +07:00

**Prompt:** Với FR-19, tạo ít nhất 40 case chỉ cho list/delete. Bao phủ phân quyền Admin, IDOR, self-delete, ID sai, payload SQL injection, privacy và schema. Đánh dấu ý tưởng cập nhật role là ngoài contract.

**Output của AI:** 40 case list/delete (`FR19-001`–`FR19-040`) với ID âm tính, role, privacy và ý tưởng postcondition.

**Quyết định của sinh viên:** Loại ý tưởng không có endpoint, cấp user dùng một lần cho case phá hủy và đặt self-delete cuối; 40 dòng cuối đều VALID.

### AI-005 — Codex — 2026-08-31 23:31:31 +07:00

**Prompt:** Audit từng dòng đã tạo là VALID/INVALID/INCOMPLETE kèm lý do; sửa dòng invalid/incomplete; khử trùng; sau đó thêm năm case do sinh viên tạo cho mỗi feature và giải thích vì sao AI bỏ sót. Biên dịch catalogue đã duyệt sang Postman/Newman.

**Output của AI:** Nhãn/lý do/bản sửa theo từng dòng và 15 dòng `HUMAN-001` tách biệt. Automation ban đầu làm lộ status mơ hồ và fixture dùng chung có thể thay đổi.

**Quyết định của sinh viên:** Giải quyết mọi điểm mơ hồ bằng SRS chuẩn tắc, sửa fixture, thêm assertion status/schema/state chính xác và chấp nhận 140/140 dòng VALID (125 AI + 15 HUMAN).

### AI-006 — Codex — 2026-09-01 17:30:59 +07:00

**Prompt:** “Hãy xem xét những thứ và nội dung trong submit còn thiếu gì so với req/2026.HW06.API Testing_Vi.md”; “bạn hãy làm tất cả luôn”; bổ sung: bằng chứng GitHub Issue phải là ảnh chụp thật, không phải console/card dựng.

**Output của AI:** Dựng lại suite 140 case có thể chạy; thực thi 467 request và 839 assertion; đối soát 98 PASS/42 FAIL thành 10 lỗi gốc; thêm run data-driven 6 dòng; thiết kế lại CI pass/đúng-một-fail; mở rộng bug register/Issue và loại tham chiếu ảnh dựng.

**Quyết định của sinh viên:** Chấp nhận thay đổi code/test/tài liệu, với điều kiện ảnh chụp là thật, sơ đồ do sinh viên tự vẽ, sau đó export PDF/XLSX và đóng ZIP.

## Thống kê output

| Nguồn output | FR-04 | FR-10 | FR-19 | Tổng |
|---|---:|---:|---:|---:|
| AI tạo, sinh viên audit | 40 | 45 | 40 | 125 |
| Sinh viên bổ sung sau audit | 5 | 5 | 5 | 15 |
| VALID và đã thực thi cuối | 45 | 50 | 45 | 140 |

Mỗi dòng có `AI source`, `Audit label`, `Audit reason`, `Corrected version`; dòng HUMAN có thêm `Why AI missed`. Không có output AI thô nào bị trình bày như nội dung do sinh viên tự tạo.
