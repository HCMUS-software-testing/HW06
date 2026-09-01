# Sổ đăng ký lỗi đã xác nhận — Thành viên 4

Tất cả lỗi được tái hiện trên SUT commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`, host `localhost`, có header MSSV `23127326`. Minh chứng Newman nằm tại `newman-full-report.html`; ánh xạ test case chi tiết nằm trong `failure-classification.md`.

| Mã lỗi | Mức độ | Kết quả mong đợi / thực tế | Test ID thất bại | GitHub Issue |
|---|---|---|---|---|
| `BUG-FR04-01` | Nghiêm trọng | Client không được đổi `role`; API trả 200 và lưu `admin`. | FR04-033, 034, 045 | [#1](https://github.com/HCMUS-software-testing/HW06/issues/1) |
| `BUG-FR04-02` | Nghiêm trọng | Hồ sơ không chứa credential; API làm lộ `password` plaintext và `reset_token`. | FR04-010 | [#2](https://github.com/HCMUS-software-testing/HW06/issues/2) |
| `BUG-FR04-03` | Cao | Phone sai trả 400 và không thay đổi dữ liệu; API trả 200 và lưu giá trị sai. | FR04-014–021 | [#35](https://github.com/HCMUS-software-testing/HW06/issues/35) |
| `BUG-FR04-04` | Cao | Empty/null/partial body được kiểm tra và giữ trường bị bỏ qua; API ghi `null` hoặc trả lỗi không nhất quán. | FR04-028, 029, 041 | [#36](https://github.com/HCMUS-software-testing/HW06/issues/36) |
| `BUG-FR10-01` | Cao | `canceled` là terminal state; API chấp nhận `canceled → delivered`. | FR10-024 | [#37](https://github.com/HCMUS-software-testing/HW06/issues/37) |
| `BUG-FR10-02` | Cao | User không được hủy đơn `shipping`; API trả 200 và lưu `canceled`. | FR10-028 | [#38](https://github.com/HCMUS-software-testing/HW06/issues/38) |
| `BUG-FR12-01` | Nghiêm trọng | API Admin bắt buộc `role=admin`; JWT User có thể liệt kê/xóa user và chuyển trạng thái đơn. | FR10-034, 047; FR19-004, 029, 031, 041 | [#3](https://github.com/HCMUS-software-testing/HW06/issues/3) |
| `BUG-FR19-01` | Trung bình | ID sai/không tồn tại/đã xóa trả 400/404; API luôn trả 200. | FR19-017–026, 033, 035–038, 042, 043 | [#39](https://github.com/HCMUS-software-testing/HW06/issues/39) |
| `BUG-FR19-02` | Cao | JWT của subject đã xóa bị từ chối; token cũ vẫn nhận 200 từ `/api/users/me`. | FR19-044 | [#40](https://github.com/HCMUS-software-testing/HW06/issues/40) |
| `BUG-FR19-03` | Cao | Admin hiện tại không được tự xóa; API trả 200 và xóa tài khoản. | FR19-045 | [#4](https://github.com/HCMUS-software-testing/HW06/issues/4) |

Mỗi Issue đã được chuẩn hóa theo cùng mẫu tiếng Việt: metadata, mô tả, bước tái hiện, actual/expected, minh chứng và nguyên nhân gốc. Ảnh bằng chứng là ảnh chụp trang GitHub Issue thật theo `evidence/README.md`.
