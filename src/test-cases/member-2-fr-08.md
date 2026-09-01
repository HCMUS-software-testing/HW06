# Test Cases & Audit - FR-08: Thanh toán / Tạo đơn hàng (Checkout)

**Thành viên:** Lê Trung Kiên (MSSV: 23127075)  
**API Endpoint:** `POST /api/checkout` (api_specification.md §4.3)  
**Header bắt buộc:** `Authorization: Bearer <userToken>`, `X-Student-Id: 23127075`  
**Nguồn đặc tả:** `eshop-sut/api_specification.md` §4.3 & `eshop-sut/README.md` FR-08, FR-09, FR-10

---

## 1. Danh Sách Test Cases AI Sinh & Kiểm Toán Audit

### Batch 1: Nghiệp vụ Thanh toán, Giỏ hàng & Mã giảm giá (18 test cases)

> **Phạm vi kiểm thử:**
> - **Checkout chuẩn & Địa chỉ giao hàng:** Địa chỉ hợp lệ, địa chỉ rỗng, địa chỉ chỉ chứa khoảng trắng, thiếu thông tin chi tiết, sđt không hợp lệ, địa chỉ quá dài.
> - **Giỏ hàng & Tồn kho:** Giỏ hàng rỗng, số lượng vượt tồn kho (out of stock), kiểm tra tự động xóa giỏ hàng sau thanh toán (Cart clearing), trạng thái đơn ban đầu là `pending` (FR-10).
> - **Tính toán số tiền & Mã giảm giá (FR-09):** Chống gian lận sửa `total_amount` từ client, áp dụng mã `SAVE10` (percent), `BIGBUY` (fixed), mã hết hạn `EXPIRED`, mã không đủ min_order_amount, mã dùng hết lượt `max_uses_per_user`, mã không tồn tại.

| STT | Test Case Name | Method | Endpoint | Request Header / Body | Expected Status | Expected Body / Response Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Checkout thành công với địa chỉ giao hàng hợp lệ | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi, TP.HCM"}` | 200 OK | Trả về JSON object chứa `order_id` (hoặc `id`), `status`: "pending", `total_amount`: 200000 |
| 2 | Checkout khi giỏ hàng rỗng (Cart is empty) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 0, "shipping_address": "123 Le Loi, TP.HCM"}` | 400 Bad Request | Thông báo lỗi giỏ hàng rỗng, không tạo đơn |
| 3 | Checkout khi số lượng sản phẩm vượt quá tồn kho (Out of Stock) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 500000, "shipping_address": "123 Le Loi, TP.HCM"}` | 400 Bad Request / 409 Conflict | Thông báo lỗi sản phẩm vượt quá số lượng trong kho |
| 4 | Checkout với địa chỉ giao hàng rỗng (Empty String) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": ""}` | 400 Bad Request | Thông báo lỗi địa chỉ giao hàng không được để trống |
| 5 | Checkout với địa chỉ giao hàng chỉ chứa khoảng trắng | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "   "}` | 400 Bad Request | Thông báo lỗi địa chỉ giao hàng không hợp lệ |
| 6 | Checkout với địa chỉ giao hàng thiếu tên đường / chi tiết | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "TP.HCM"}` | 400 Bad Request / 200 OK | Kiểm tra địa chỉ có đủ thông tin giao hàng |
| 7 | Checkout với số điện thoại giao hàng sai định dạng | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "phone": "12345"}` | 400 Bad Request | Thông báo lỗi số điện thoại không hợp lệ (phải từ 10-11 số, bắt đầu bằng 0) |
| 8 | Checkout với địa chỉ giao hàng quá dài (> 500 ký tự) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "aaaa..." (500+ chars)}` | 400 Bad Request | Server từ chối địa chỉ vượt quá độ dài tối đa |
| 9 | Kiểm tra chống gian lận giá trị `total_amount` từ Client | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 1000, "shipping_address": "123 Le Loi, TP.HCM"}` *(Giỏ hàng thực tế 200,000đ)* | 200 OK | Backend tự động tính lại tổng tiền 200,000đ theo giỏ hàng thực tế; không dùng giá trị 1,000đ của Client |
| 10 | Checkout áp dụng mã giảm giá hợp lệ theo phần trăm (`SAVE10`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 450000, "shipping_address": "123 Le Loi", "coupon_code": "SAVE10"}` | 200 OK | Đơn hàng áp dụng giảm 10% trên tổng đơn 500,000đ, số tiền cuối cùng = 450,000đ |
| 11 | Checkout áp dụng mã giảm giá cố định hợp lệ (`BIGBUY`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 450000, "shipping_address": "123 Le Loi", "coupon_code": "BIGBUY"}` | 200 OK | Đơn hàng áp dụng giảm 50,000đ trên đơn 500,000đ, số tiền cuối cùng = 450,000đ |
| 12 | Checkout với mã giảm giá đã hết hạn (`EXPIRED`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 500000, "shipping_address": "123 Le Loi", "coupon_code": "EXPIRED"}` | 400 Bad Request | Thông báo lỗi mã giảm giá đã hết hạn sử dụng (C2) |
| 13 | Checkout với mã giảm giá không đủ giá trị đơn hàng tối thiểu | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "coupon_code": "BIGBUY"}` *(Đơn 200k < min 500k)* | 400 Bad Request | Thông báo lỗi chưa đạt giá trị đơn hàng tối thiểu để dùng mã (C3) |
| 14 | Checkout với mã giảm giá đã dùng hết số lần cho phép (`max_uses_per_user`) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 400000, "shipping_address": "123 Le Loi", "coupon_code": "SAVE10"}` | 400 Bad Request | Thông báo lỗi bạn đã dùng hết số lần cho phép của mã giảm giá này (C5) |
| 15 | Checkout với mã giảm giá không tồn tại trong CSDL | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "coupon_code": "INVALID999"}` | 400 Bad Request / 404 Not Found | Thông báo lỗi mã giảm giá không tồn tại (C1) |
| 16 | Kiểm tra tự động xóa giỏ hàng sau khi checkout thành công | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Sau khi checkout thành công, gọi `GET /api/cart` trả về mảng giỏ hàng rỗng `[]` |
| 17 | Kiểm tra trạng thái đơn hàng ban đầu luôn là `pending` | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi"}` | 200 OK | Thuộc tính `status` trong đơn hàng mới tạo phải bằng `"pending"` (FR-10) |
| 18 | Checkout kèm ghi chú đơn hàng (Order Notes) | POST | `/api/checkout` | Header: `Bearer <userToken>`<br>Body: `{"total_amount": 200000, "shipping_address": "123 Le Loi", "notes": "Giao giờ hành chính"}` | 200 OK | Lưu thông tin đơn hàng thành công kèm ghi chú giao hàng |

---

### Bảng Kiểm Toán Audit — Batch 1 (18 Test Cases)

| STT | Test Case ID | Trạng thái Audit | Lý do Audit & Hướng sửa đổi |
| --- | --- | --- | --- |
| 1 | TC-FR08-AI-001 | [Manual by user] | [Manual by user] |
| 2 | TC-FR08-AI-002 | [Manual by user] | [Manual by user] |
| 3 | TC-FR08-AI-003 | [Manual by user] | [Manual by user] |
| 4 | TC-FR08-AI-004 | [Manual by user] | [Manual by user] |
| 5 | TC-FR08-AI-005 | [Manual by user] | [Manual by user] |
| 6 | TC-FR08-AI-006 | [Manual by user] | [Manual by user] |
| 7 | TC-FR08-AI-007 | [Manual by user] | [Manual by user] |
| 8 | TC-FR08-AI-008 | [Manual by user] | [Manual by user] |
| 9 | TC-FR08-AI-009 | [Manual by user] | [Manual by user] |
| 10 | TC-FR08-AI-010 | [Manual by user] | [Manual by user] |
| 11 | TC-FR08-AI-011 | [Manual by user] | [Manual by user] |
| 12 | TC-FR08-AI-012 | [Manual by user] | [Manual by user] |
| 13 | TC-FR08-AI-013 | [Manual by user] | [Manual by user] |
| 14 | TC-FR08-AI-014 | [Manual by user] | [Manual by user] |
| 15 | TC-FR08-AI-015 | [Manual by user] | [Manual by user] |
| 16 | TC-FR08-AI-016 | [Manual by user] | [Manual by user] |
| 17 | TC-FR08-AI-017 | [Manual by user] | [Manual by user] |
| 18 | TC-FR08-AI-018 | [Manual by user] | [Manual by user] |

---

*(Batch 2: Bảo mật Authentication/IDOR & Response Schema — 17 test cases sẽ được bổ sung ở prompt tiếp theo)*

---

## 2. Test Cases Tự Bổ Sung (Human-designed >= 5 cases)

| Test Case ID | Tên kịch bản | Loại (Bảo mật / Chuyển trạng thái / Biên) | Input Parameters & Steps | Expected Result | Lý do AI bỏ sót |
| --- | --- | --- | --- | --- | --- |
| *(Sẽ được bổ sung sau khi hoàn thành kiểm toán audit batch 1 + batch 2)* | | | | | |
