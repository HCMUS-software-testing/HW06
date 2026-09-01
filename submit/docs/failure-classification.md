# Phân loại kết quả Newman — full conformance run

- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`
- Catalogue cases: **140**; PASS: **98**; FAIL: **42**
- HTTP requests (gồm fixture/postcondition): **467**
- Assertions: **839**; failed assertions: **63**
- Fixture/request errors: **0**. Mỗi case FAIL bên dưới được quy về một lỗi sản phẩm, không phải lỗi dữ liệu test.

| Bug ID | Root defect | Failed catalogue cases | Số case |
|---|---|---|---:|
| `BUG-04-001` | Profile update accepts protected role field | `FR04-033`, `FR04-034`, `FR04-045` | 3 |
| `BUG-04-002` | Profile response exposes password/reset-token fields | `FR04-010` | 1 |
| `BUG-04-003` | Profile update accepts invalid phone partitions | `FR04-014`, `FR04-015`, `FR04-016`, `FR04-017`, `FR04-018`, `FR04-019`, `FR04-020`, `FR04-021` | 8 |
| `BUG-04-004` | Profile update lacks safe partial/body validation | `FR04-028`, `FR04-029`, `FR04-041` | 3 |
| `BUG-10-001` | Canceled order can transition to delivered | `FR10-024` | 1 |
| `BUG-10-002` | User can cancel an order already in shipping | `FR10-028` | 1 |
| `BUG-04-005` | Admin endpoints do not enforce admin role | `FR10-034`, `FR10-047`, `FR19-004`, `FR19-029`, `FR19-031`, `FR19-041` | 6 |
| `BUG-19-001` | Delete user returns success for invalid/missing/repeated targets | `FR19-017`, `FR19-018`, `FR19-019`, `FR19-020`, `FR19-021`, `FR19-022`, `FR19-023`, `FR19-024`, `FR19-025`, `FR19-026`, `FR19-033`, `FR19-035`, `FR19-036`, `FR19-037`, `FR19-038`, `FR19-042`, `FR19-043` | 17 |
| `BUG-19-002` | Deleted user's JWT remains accepted | `FR19-044` | 1 |
| `BUG-04-006` | Admin can delete their own account | `FR19-045` | 1 |

## Quy tắc phân loại

Case chỉ PASS khi toàn bộ status, schema, header và postcondition của case đều pass. Case âm tính nhận response trái oracle vẫn là FAIL; tên case 'negative' không biến nó thành expected failure.
