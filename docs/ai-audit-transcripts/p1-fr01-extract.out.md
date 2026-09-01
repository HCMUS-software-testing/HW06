AI output (rút gọn — kết quả được người rà rồi nạp vào lớp parser của skill)

Tham số:
- name: string, required theo spec, không ràng buộc độ dài.
- email: string, required, định dạng email, UNIQUE trong users.
- password: string, required, policy: >=8, 1 hoa, 1 thường, 1 số, 1 ký tự @$!%*?&.

Actor/role: public (không cần token). API không nhận header Authorization.
Status theo spec: 200 (thành công, trả message + id), 400 (validate fail), 409 (email trùng).
Response schema: 200 -> {message, id}; error -> thành công phải là JSON có thông báo, không phải stack trace.

Ghi chú của người: SUT thật không validate gì — ghi nhận để tách suite discovery. Parser skill phải trích đúng 3 field + 2 rule (email_unique, password_policy).
