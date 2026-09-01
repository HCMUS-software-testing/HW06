# Phân loại kết quả Newman — lần conformance đầy đủ

- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`
- Catalogue cases: **140**; PASS: **98**; FAIL: **42**
- HTTP requests (gồm fixture/postcondition): **467**
- Assertions: **839**; failed assertions: **63**
- Fixture/request errors: **0**. Mỗi case FAIL bên dưới được quy về một lỗi sản phẩm, không phải lỗi dữ liệu test.

| Mã lỗi | Lỗi gốc | Test case thất bại | Số case |
|---|---|---|---:|
| `BUG-FR04-01` | Cập nhật hồ sơ chấp nhận trường role được bảo vệ | `FR04-033`, `FR04-034`, `FR04-045` | 3 |
| `BUG-FR04-02` | Response hồ sơ làm lộ password và reset_token | `FR04-010` | 1 |
| `BUG-FR04-03` | Cập nhật hồ sơ chấp nhận các phân hoạch phone không hợp lệ | `FR04-014`, `FR04-015`, `FR04-016`, `FR04-017`, `FR04-018`, `FR04-019`, `FR04-020`, `FR04-021` | 8 |
| `BUG-FR04-04` | Cập nhật hồ sơ thiếu kiểm tra body và partial update an toàn | `FR04-028`, `FR04-029`, `FR04-041` | 3 |
| `BUG-FR10-01` | Đơn đã hủy có thể chuyển sang đã giao | `FR10-024` | 1 |
| `BUG-FR10-02` | Người dùng có thể hủy đơn đang vận chuyển | `FR10-028` | 1 |
| `BUG-FR12-01` | API Admin không bắt buộc role admin | `FR10-034`, `FR10-047`, `FR19-004`, `FR19-029`, `FR19-031`, `FR19-041` | 6 |
| `BUG-FR19-01` | Xóa user trả success với target sai, không tồn tại hoặc lặp lại | `FR19-017`, `FR19-018`, `FR19-019`, `FR19-020`, `FR19-021`, `FR19-022`, `FR19-023`, `FR19-024`, `FR19-025`, `FR19-026`, `FR19-033`, `FR19-035`, `FR19-036`, `FR19-037`, `FR19-038`, `FR19-042`, `FR19-043` | 17 |
| `BUG-FR19-02` | JWT của user đã bị xóa vẫn được chấp nhận | `FR19-044` | 1 |
| `BUG-FR19-03` | Admin có thể tự xóa tài khoản | `FR19-045` | 1 |

## Quy tắc phân loại

Case chỉ PASS khi toàn bộ status, schema, header và postcondition của case đều pass. Case âm tính nhận response trái oracle vẫn là FAIL; tên case 'negative' không biến nó thành expected failure.
