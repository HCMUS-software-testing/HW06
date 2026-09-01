#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: Automated GitHub Issue Updater (Full Vietnamese & Reproduce Steps)
Author: Lam Huu Khanh (MSSV: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing

Description:
  Updates all 12 GitHub Issues on HCMUS-software-testing/HW06 with:
  - Full Vietnamese diacritics and professional technical structure.
  - Zero decorative emojis/icons in titles and headings.
  - Comprehensive Steps to Reproduce, Request/Response payloads, and Root Causes.
  - Embedded real test execution screenshots directly from branch `khanh`.
=============================================================================
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.error

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

REPO_OWNER = "HCMUS-software-testing"
REPO_NAME = "HW06"
BRANCH = "khanh"
BASE_IMG_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/reports/screenshots/github-issues"

ISSUES_DATA = [
    {
        "issue_number": 5,
        "id": "BUG-FR02-01",
        "title": "[BUG-FR02-01] Bộ đếm login_attempts tăng 2 đơn vị mỗi lần đăng nhập sai",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR02-01`
- **Phân hệ:** Pool A (FR-02: Đăng nhập & Khóa tài khoản)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** High
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Theo đặc tả SRS Mục 2 (FR-02): *"Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên đúng 1 đơn vị. Nếu đăng nhập sai từ 3 lần trở lên liên tiếp, tài khoản bị tạm khóa."* 
Tuy nhiên, thực tế khi người dùng nhập sai mật khẩu 1 lần, bộ đếm trong CSDL SQLite tăng từ `0` lên `2`. Chỉ cần sai 2 lần là bộ đếm đạt `4 >= 3` và tài khoản bị khóa ngay lập tức.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/login` với body:
   ```json
   {{ "email": "lockout_target@eshop.com", "password": "WrongPassword1!" }}
   ```
2. Kiểm tra `login_attempts` trong SQLite: giá trị tăng vọt lên `2`.
3. Gửi tiếp lần 2 với mật khẩu sai `WrongPassword2!`.
4. Hệ thống chuyển tài khoản sang trạng thái khóa và trả về HTTP `403 Forbidden`.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** Tài khoản bị khóa chỉ sau 2 lần nhập sai (do `login_attempts + 2`).
- **Mong đợi (Expected):** Sau lần 1: `login_attempts = 1`, sau lần 2: `login_attempts = 2`, sau lần 3 mới bị khóa.

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR02-01]({BASE_IMG_URL}/issue-1.png)

### Nguyên nhân gốc & Đề xuất khắc phục (Root Cause & Fix)
Tại `server.js:L54`:
```javascript
// Lỗi hiện tại:
const newAttempts = user.login_attempts + 2;

// Đề xuất sửa:
const newAttempts = (user.login_attempts || 0) + 1;
```""",
        "labels": ["bug", "FR-02", "severity:high"]
    },
    {
        "issue_number": 6,
        "id": "BUG-FR02-02",
        "title": "[BUG-FR02-02] Thời gian khóa tài khoản là 180s (3 phút) thay vì 30s",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR02-02`
- **Phân hệ:** Pool A (FR-02: Đăng nhập & Khóa tài khoản)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** Medium
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
SRS FR-02 quy định trong môi trường thử nghiệm: *"Thời gian tạm khóa tài khoản khi đăng nhập sai từ 3 lần trở lên là 30 giây."* 
Mã nguồn backend thiết lập thời gian khóa là `180000 ms` (3 phút).

### Các bước tái hiện (Steps to Reproduce)
1. Gửi liên tiếp 2 request sai đến `POST http://localhost:3000/api/login` với email `lockout_target@eshop.com`.
2. Kiểm tra giá trị trường `locked_until` trong SQLite: chênh lệch `180000ms` (3 phút) so với thời điểm hiện tại.
3. Gửi tiếp request đăng nhập trong vòng 3 phút tiếp theo: luôn nhận `403 Forbidden`.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** `locked_until = Date.now() + 180000ms` (Bị khóa kéo dài 180 giây / 3 phút).
- **Mong đợi (Expected):** `locked_until = Date.now() + 30000ms` (Chỉ bị khóa 30 giây).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR02-02]({BASE_IMG_URL}/issue-2.png)

### Nguyên nhân gốc & Đề xuất khắc phục
Tại `server.js:L57`:
```javascript
// Lỗi hiện tại:
lockedUntil = new Date(Date.now() + 180000).toISOString();

// Đề xuất sửa:
lockedUntil = new Date(Date.now() + 30000).toISOString();
```""",
        "labels": ["bug", "FR-02", "severity:medium"]
    },
    {
        "issue_number": 7,
        "id": "BUG-FR02-03",
        "title": "[BUG-FR02-03] Thiếu validation định dạng Email, trả về 401 thay vì 400 Bad Request",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR02-03`
- **Phân hệ:** Pool A (FR-02: Đăng nhập & Khóa tài khoản)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** Low
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Khi gửi body đăng nhập với email sai định dạng (ví dụ `notanemail` không có ký tự `@` hoặc chuỗi rỗng), server không thực hiện xác thực định dạng đầu vào (Input Format Validation) ở tầng Controller mà trực tiếp truy vấn CSDL SQLite rồi trả về `401 Unauthorized`.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/login` với body:
   ```json
   {{ "email": "invalid-email-format", "password": "TestPassword123!" }}
   ```
2. Quan sát HTTP Status Code trả về từ server.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** HTTP `401 Unauthorized` với message `"Invalid email or password"`.
- **Mong đợi (Expected):** HTTP `400 Bad Request` với message `"Email format is invalid"`.

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR02-03]({BASE_IMG_URL}/issue-3.png)

### Nguyên nhân gốc & Đề xuất khắc phục
Tại `server.js:L33-40`: Route handler thiếu middleware kiểm tra regex định dạng email trước khi gọi `db.get`.""",
        "labels": ["bug", "FR-02", "severity:low"]
    },
    {
        "issue_number": 8,
        "id": "BUG-FR02-04",
        "title": "[BUG-FR02-04] Lỗ hổng bảo mật SEC-01: Response đăng nhập trả về trường password plaintext",
        "body": f"""### Thông tin lỗi (Security Defect Metadata)
- **Mã lỗi:** `BUG-FR02-04` (Lỗ hổng OWASP API Security `SEC-01` - Broken Object Property Level Authorization / Sensitive Data Exposure)
- **Phân hệ:** Pool A (FR-02: Đăng nhập)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** Critical
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗ hổng bảo mật (Description)
Khi người dùng đăng nhập thành công, response JSON trả về nguyên vẹn toàn bộ object `user` từ câu lệnh `SELECT * FROM users`, bao gồm cả trường `password` dạng plaintext (`"password": "Admin123!"`). Kẻ tấn công hoặc middleware trung gian có thể dễ dàng đọc trộm mật khẩu gốc của tài khoản.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/login` với thông tin Admin:
   ```json
   {{ "email": "admin@eshop.com", "password": "Admin123!" }}
   ```
2. Quan sát Response JSON trả về trong tab Body.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):**
  ```json
  {{
    "message": "Login successful",
    "token": "eyJhbGciOi...",
    "user": {{
      "id": 1,
      "email": "admin@eshop.com",
      "password": "Admin123!",
      "role": "admin"
    }}
  }}
  ```
- **Mong đợi (Expected):** Object `user` tuyệt đối **KHÔNG ĐƯỢC CHỨA** trường `password`.

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR02-04]({BASE_IMG_URL}/issue-4.png)

### Nguyên nhân gốc & Đề xuất khắc phục
Tại `server.js:L52`:
```javascript
// Lỗi hiện tại:
res.json({{ message: "Login successful", token, user }});

// Đề xuất sửa:
const {{ password: _, ...safeUser }} = user;
res.json({{ message: "Login successful", token, user: safeUser }});
```""",
        "labels": ["bug", "security", "FR-02", "severity:critical"]
    },
    {
        "issue_number": 9,
        "id": "BUG-FR07-01",
        "title": "[BUG-FR07-01] Backend không kiểm tra số lượng âm hoặc bằng 0 (quantity <= 0)",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-01`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `POST /api/cart`
- **Mức độ nghiêm trọng:** High
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Endpoint `POST /api/cart` không kiểm tra điều kiện `quantity > 0`. Khi client gửi request thêm sản phẩm với số lượng âm (`quantity: -5`), backend vẫn chấp nhận thêm vào giỏ hàng và trả về `200 OK`.

### Các bước tái hiện (Steps to Reproduce)
1. Lấy User Token hợp lệ từ `POST /api/login`.
2. Gửi request `POST http://localhost:3000/api/cart` với Header `Authorization: Bearer <user_token>` và body:
   ```json
   {{ "id": 1, "name": "iPhone 15", "price": 30000000, "quantity": -5 }}
   ```
3. Quan sát kết quả response và gửi tiếp `GET /api/cart`.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** HTTP `200 OK` (`"message": "Added to cart"`). Giỏ hàng chứa item có `quantity = -5`.
- **Mong đợi (Expected):** HTTP `400 Bad Request` (`"error": "Số lượng sản phẩm phải lớn hơn 0"`).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR07-01]({BASE_IMG_URL}/issue-5.png)

### Nguyên nhân gốc & Đề xuất khắc phục
Tại `server.js:L290-295`:
```javascript
// Lỗi hiện tại:
userCarts[userId].push(req.body); // Không validate req.body.quantity > 0

// Đề xuất sửa:
const {{ quantity }} = req.body;
if (!quantity || quantity <= 0 || !Number.isInteger(quantity)) {{
  return res.status(400).json({{ error: "Số lượng sản phẩm phải là số nguyên dương" }});
}}
```""",
        "labels": ["bug", "FR-07", "severity:high"]
    },
    {
        "issue_number": 10,
        "id": "BUG-FR07-02",
        "title": "[BUG-FR07-02] Thêm sản phẩm số lượng = 0 vẫn được server chấp nhận",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-02`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `POST /api/cart`
- **Mức độ nghiêm trọng:** Medium
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Khi client gửi request thêm sản phẩm vào giỏ hàng với `quantity = 0`, server không từ chối mà vẫn trả về `200 OK` và thêm item rỗng vào mảng giỏ hàng của người dùng.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/cart` với Header `Authorization: Bearer <user_token>`:
   ```json
   {{ "id": 1, "name": "iPhone 15", "price": 30000000, "quantity": 0 }}
   ```
2. Server trả về `200 OK`.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** HTTP `200 OK`.
- **Mong đợi (Expected):** HTTP `400 Bad Request` (`"Số lượng phải lớn hơn 0"`).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR07-02]({BASE_IMG_URL}/issue-6.png)

### Vị trí mã nguồn
Tại `server.js:L290-295`, thiếu điều kiện kiểm tra `if (quantity === 0)`.""",
        "labels": ["bug", "FR-07", "severity:medium"]
    },
    {
        "issue_number": 11,
        "id": "BUG-FR07-03",
        "title": "[BUG-FR07-03] Thiếu hoàn toàn API Cập nhật số lượng giỏ hàng (PUT /api/cart)",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-03`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `PUT /api/cart`
- **Mức độ nghiêm trọng:** Critical (Missing Feature)
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Đặc tả SRS yêu cầu API cập nhật số lượng item trong giỏ hàng (`PUT /api/cart`), nhưng backend hoàn toàn chưa cài đặt route này. Khi client gọi đến, server trả về `404 Not Found`.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `PUT http://localhost:3000/api/cart` với Header `Authorization: Bearer <user_token>`:
   ```json
   {{ "id": 1, "quantity": 5 }}
   ```
2. Quan sát mã trạng thái HTTP trả về.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** HTTP `404 Not Found`.
- **Mong đợi (Expected):** HTTP `200 OK` (`"message": "Cart updated successfully"`).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR07-03]({BASE_IMG_URL}/issue-7.png)

### Nguyên nhân gốc
Trong `server.js`, phân hệ Cart chỉ có duy nhất 2 route là `GET /api/cart` và `POST /api/cart`, thiếu hoàn toàn handler cho `app.put('/api/cart', ...)`.""",
        "labels": ["bug", "FR-07", "severity:critical"]
    },
    {
        "issue_number": 12,
        "id": "BUG-FR07-04",
        "title": "[BUG-FR07-04] Thiếu hoàn toàn API Xóa item khỏi giỏ hàng (DELETE /api/cart/:id)",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-04`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `DELETE /api/cart/:id`
- **Mức độ nghiêm trọng:** Critical (Missing Feature)
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Đặc tả SRS yêu cầu endpoint xóa một sản phẩm cụ thể ra khỏi giỏ hàng (`DELETE /api/cart/:id`), nhưng route này hoàn toàn vắng mặt trong backend.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `DELETE http://localhost:3000/api/cart/1` kèm Header `Authorization: Bearer <user_token>`.
2. Quan sát kết quả trả về từ server.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** HTTP `404 Not Found`.
- **Mong đợi (Expected):** HTTP `200 OK` (`"message": "Item removed from cart"`).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR07-04]({BASE_IMG_URL}/issue-8.png)

### Nguyên nhân gốc
Trong `server.js`, hoàn toàn không có định nghĩa `app.delete('/api/cart/:id', ...)`.""",
        "labels": ["bug", "FR-07", "severity:critical"]
    },
    {
        "issue_number": 13,
        "id": "BUG-FR15-01",
        "title": "[BUG-FR15-01] Lỗ hổng bảo mật SEC-03: Thiếu middleware xác thực Admin (authenticateToken) trên CRUD sản phẩm",
        "body": f"""### Thông tin lỗi (Security Defect Metadata)
- **Mã lỗi:** `BUG-FR15-01` (OWASP API Security `SEC-03` - Broken Function Level Authorization)
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm CRUD)
- **API Endpoint:** `POST/PUT/DELETE /api/products`
- **Mức độ nghiêm trọng:** Critical
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗ hổng bảo mật (Description)
Theo đặc tả SRS FR-15: Chỉ có người dùng có vai trò **Admin** mới được phép Thêm mới, Cập nhật và Xóa sản phẩm. Tuy nhiên, backend Express **hoàn toàn quên gắn middleware `authenticateToken`** vào cả 3 route này. Bất kỳ ai không cần đăng nhập cũng có thể thêm/sửa/xóa sản phẩm trong CSDL.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/products` mà **không đính kèm bất kỳ Token xác thực nào** (No Auth):
   ```json
   {{ "name": "Unauthorized Product", "price": 1000, "category_id": 1 }}
   ```
2. Gửi tiếp request `DELETE http://localhost:3000/api/products/6` không có Token.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** Server trả về `200 OK` và thực thi thêm/xóa thành công trong SQLite.
- **Mong đợi (Expected):** HTTP `401 Unauthorized` (nếu không có token) hoặc `403 Forbidden` (nếu là user thường).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR15-01]({BASE_IMG_URL}/issue-9.png)

### Nguyên nhân gốc & Đề xuất khắc phục
Tại `server.js:L167, L179, L191`:
```javascript
// Lỗi hiện tại:
app.post("/api/products", (req, res) => {{ ... }});
app.put("/api/products/:id", (req, res) => {{ ... }});
app.delete("/api/products/:id", (req, res) => {{ ... }});

// Đề xuất sửa:
app.post("/api/products", authenticateToken, requireAdmin, (req, res) => {{ ... }});
app.put("/api/products/:id", authenticateToken, requireAdmin, (req, res) => {{ ... }});
app.delete("/api/products/:id", authenticateToken, requireAdmin, (req, res) => {{ ... }});
```""",
        "labels": ["bug", "security", "FR-15", "severity:critical"]
    },
    {
        "issue_number": 14,
        "id": "BUG-FR15-02",
        "title": "[BUG-FR15-02] Ép kiểu price sang String ở các sản phẩm có ID chẵn",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR15-02`
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `GET /api/products/:id`
- **Mức độ nghiêm trọng:** Medium
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Khi gọi API lấy chi tiết sản phẩm, nếu sản phẩm có `id` là số chẵn (ví dụ ID 2, ID 4, ID 6), server cố tình ép kiểu trường `price` sang kiểu String (`"28000000"` có dấu ngoặc kép) thay vì kiểu số Number (`28000000`), vi phạm hợp đồng dữ liệu OpenAPI/JSON Schema.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `GET http://localhost:3000/api/products/2`.
2. Quan sát trường `price` trong response JSON trả về.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** `"price": "28000000"` (kiểu String).
- **Mong đợi (Expected):** `"price": 28000000` (kiểu Number).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR15-02]({BASE_IMG_URL}/issue-10.png)

### Nguyên nhân gốc & Đề xuất khắc phục
Tại `server.js:L162`:
```javascript
// Đoạn code gây lỗi:
if (row.id % 2 === 0) {{
    row.price = String(row.price); // Cố tình ép kiểu sang chuỗi
}}

// Đề xuất sửa: Xóa bỏ hoàn toàn khối if trên để giữ nguyên kiểu số Number.
```""",
        "labels": ["bug", "FR-15", "severity:medium"]
    },
    {
        "issue_number": 15,
        "id": "BUG-FR15-03",
        "title": "[BUG-FR15-03] Cho phép tạo sản phẩm với giá âm (price < 0)",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR15-03`
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `POST /api/products`
- **Mức độ nghiêm trọng:** High
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Backend không kiểm tra ràng buộc giá sản phẩm `price > 0`. Khi gửi request tạo sản phẩm với `price = -500000`, server vẫn chèn vào CSDL và trả về `200 OK`.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/products` với body:
   ```json
   {{ "name": "Sản phẩm giá âm", "price": -500000, "category_id": 1 }}
   ```
2. Quan sát kết quả trả về từ server.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** HTTP `200 OK` (`"message": "Product created"`).
- **Mong đợi (Expected):** HTTP `400 Bad Request` (`"error": "Giá sản phẩm phải lớn hơn 0"`).

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR15-03]({BASE_IMG_URL}/issue-11.png)

### Nguyên nhân gốc
Tại `server.js:L167-176`: Handler nhận dữ liệu từ `req.body` và truyền thẳng vào câu lệnh `INSERT INTO products` mà không có validation `if (price <= 0)`.""",
        "labels": ["bug", "FR-15", "severity:high"]
    },
    {
        "issue_number": 16,
        "id": "BUG-FR15-04",
        "title": "[BUG-FR15-04] Xóa/Sửa sản phẩm không cần quyền Admin",
        "body": f"""### Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR15-04`
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `DELETE /api/products/:id`
- **Mức độ nghiêm trọng:** Critical
- **Người báo cáo:** Lâm Hữu Khánh (MSSV: `23127205`)

### Mô tả lỗi (Description)
Bất kỳ request `DELETE /api/products/:id` nào gửi lên mà không có Token Authorization hoặc chỉ là User thông thường đều xóa được sản phẩm trong CSDL SQLite.

### Các bước tái hiện (Steps to Reproduce)
1. Gửi request `DELETE http://localhost:3000/api/products/6` không kèm Header Authorization.
2. Gửi tiếp request `GET http://localhost:3000/api/products/6` để xác nhận.

### Kết quả thực tế vs Kết quả mong đợi
- **Thực tế (Actual):** Sản phẩm ID 6 bị xóa sạch khỏi CSDL với HTTP `200 OK`.
- **Mong đợi (Expected):** HTTP `401 Unauthorized` hoặc `403 Forbidden`.

### Minh chứng kiểm thử thực tế (Test Execution Screenshot)
![Minh chứng BUG-FR15-04]({BASE_IMG_URL}/issue-12.png)

### Nguyên nhân gốc
Tại `server.js:L191`: Route `app.delete('/api/products/:id', ...)` thiếu hoàn toàn middleware xác thực và phân quyền Admin.""",
        "labels": ["bug", "security", "FR-15", "severity:critical"]
    }
]


def update_issue(token: str, issue_number: int, data: dict) -> bool:
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    payload = json.dumps({
        "title": data["title"],
        "body": data["body"],
        "labels": data["labels"]
    }).encode("utf-8")

    req = urllib.request.Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "HW06-API-Testing-Updater"
        },
        method="PATCH"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[-] HTTP {e.code} Error updating #{issue_number}: {err_msg}")
        return False
    except Exception as e:
        print(f"[-] Exception updating #{issue_number}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Update 12 GitHub Issues with full Vietnamese and detailed steps")
    parser.add_argument("--token", "-t", required=True, help="GitHub Personal Access Token")
    args = parser.parse_args()

    print("=" * 70)
    print(f"  UPDATING 12 GITHUB ISSUES (FULL VIETNAMESE & STEPS) ON {REPO_OWNER}/{REPO_NAME}")
    print("=" * 70)

    success_count = 0
    for item in ISSUES_DATA:
        num = item["issue_number"]
        print(f"\n[*] Updating Issue #{num} ({item['id']})...")
        if update_issue(args.token, num, item):
            print(f"    [+] Successfully updated #{num} ({item['title'][:40]}...)")
            success_count += 1
        else:
            print(f"    [-] Failed to update #{num}")
        time.sleep(1)

    print("\n" + "=" * 70)
    print(f"  SUMMARY: Successfully updated {success_count}/12 issues on GitHub!")
    print("=" * 70)


if __name__ == "__main__":
    main()
