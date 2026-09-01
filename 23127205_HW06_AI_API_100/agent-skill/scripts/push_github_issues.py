#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: Automated GitHub Issue Publisher
Author: Lam Huu Khanh (MSSV: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing

Description:
  Automates publishing all 12 SUT bug reports to GitHub Issues via GitHub REST API v3.
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
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

ISSUES_DATA = [
    {
        "id": "BUG-FR02-01",
        "title": "[BUG-FR02-01] Bộ đếm login_attempts tăng 2 đơn vị mỗi lần đăng nhập sai",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR02-01`
- **Phân hệ:** Pool A (FR-02: Đăng nhập & Khóa tài khoản)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** High
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi (Description)
Theo đặc tả SRS Mục 2 (FR-02): *"Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên đúng 1 đơn vị. Nếu đăng nhập sai từ 3 lần trở lên liên tiếp, tài khoản bị tạm khóa."* 
Tuy nhiên, thực tế khi người dùng nhập sai mật khẩu 1 lần, bộ đếm trong CSDL SQLite tăng từ `0` lên `2`. Chỉ cần sai 2 lần là bộ đếm đạt `4 >= 3` và tài khoản bị khóa ngay lập tức.

### 🔁 Các bước tái hiện (Steps to Reproduce)
1. Gửi request `POST http://localhost:3000/api/login` với body:
   ```json
   { "email": "lockout_target@eshop.com", "password": "WrongPassword1!" }
   ```
2. Kiểm tra `login_attempts` trong SQLite: giá trị tăng lên `2`.
3. Gửi tiếp lần 2 với mật khẩu sai `WrongPassword2!`.
4. Hệ thống chuyển tài khoản sang trạng thái khóa và trả về HTTP `403 Forbidden`.

### 🔍 Kết quả thực tế vs Mong đợi
- **Thực tế (Actual):** Khóa sau 2 lần sai.
- **Mong đợi (Expected):** Lần 1: `login_attempts = 1`, Lần 2: `login_attempts = 2`, Lần 3 mới bị khóa.

### 🧑‍💻 Nguyên nhân gốc & Đề xuất sửa (Root Cause & Fix)
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
        "id": "BUG-FR02-02",
        "title": "[BUG-FR02-02] Thời gian khóa tài khoản là 180s (3 phút) thay vì 30s",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR02-02`
- **Phân hệ:** Pool A (FR-02: Đăng nhập & Khóa tài khoản)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** Medium
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi (Description)
SRS FR-02 quy định trong môi trường thử nghiệm: *"Thời gian tạm khóa tài khoản khi đăng nhập sai từ 3 lần trở lên là 30 giây."* 
Mã nguồn backend thiết lập thời gian khóa là `180000 ms` (3 phút).

### 🔍 Kết quả thực tế vs Mong đợi
- **Thực tế (Actual):** `locked_until = Date.now() + 180000ms` (3 phút).
- **Mong đợi (Expected):** `locked_until = Date.now() + 30000ms` (30 giây).

### 🧑‍💻 Nguyên nhân gốc & Đề xuất sửa
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
        "id": "BUG-FR02-03",
        "title": "[BUG-FR02-03] Thiếu validation định dạng Email, trả về 401 thay vì 400 Bad Request",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR02-03`
- **Phân hệ:** Pool A (FR-02: Đăng nhập & Khóa tài khoản)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** Low
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Khi gửi email sai định dạng (ví dụ `notanemail` không có `@`), server không kiểm tra regex ở Controller mà truy vấn CSDL SQLite rồi trả về `401 Unauthorized`.
- **Thực tế:** HTTP `401 Unauthorized` (`Invalid email or password`).
- **Mong đợi:** HTTP `400 Bad Request` (`Invalid email format`).

### 🧑‍💻 Vị trí mã nguồn
Tại `server.js:L33-40`, thiếu middleware validate email regex.""",
        "labels": ["bug", "FR-02", "severity:low"]
    },
    {
        "id": "BUG-FR02-04",
        "title": "[BUG-FR02-04] Lỗ hổng bảo mật SEC-01: Response đăng nhập trả về trường password plaintext",
        "body": """### 📌 Thông tin lỗi (Security Defect Metadata)
- **Mã lỗi:** `BUG-FR02-04` (Lỗ hổng OWASP API Security `SEC-01` - Broken Object Property Level Authorization)
- **Phân hệ:** Pool A (FR-02: Đăng nhập)
- **API Endpoint:** `POST /api/login`
- **Mức độ nghiêm trọng:** **Critical**
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 🚨 Mô tả lỗ hổng bảo mật
Khi người dùng đăng nhập thành công, response JSON trả về nguyên vẹn toàn bộ object `user` bao gồm cả trường `password` dạng plaintext (`"password": "Admin123!"`). Kẻ tấn công hoặc middleware trung gian có thể đánh cắp mật khẩu gốc của tài khoản.

### 🧑‍💻 Nguyên nhân gốc & Đề xuất sửa
Tại `server.js:L52`:
```javascript
// Lỗi hiện tại:
res.json({ message: "Login successful", token, user });

// Đề xuất sửa (Loại bỏ trường password trước khi trả về):
const { password: _, ...safeUser } = user;
res.json({ message: "Login successful", token, user: safeUser });
```""",
        "labels": ["bug", "security", "FR-02", "severity:critical"]
    },
    {
        "id": "BUG-FR07-01",
        "title": "[BUG-FR07-01] Backend không kiểm tra số lượng âm hoặc bằng 0 (quantity <= 0)",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-01`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `POST /api/cart`
- **Mức độ nghiêm trọng:** High
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Endpoint `POST /api/cart` không xác thực trường `quantity > 0`. Khi client gửi `{"id": 1, "quantity": -5}`, server vẫn chấp nhận và thêm vào giỏ hàng với HTTP `200 OK`.
- **Thực tế:** HTTP `200 OK`.
- **Mong đợi:** HTTP `400 Bad Request` (`Quantity must be greater than 0`).

### 🧑‍💻 Vị trí mã nguồn
Tại `server.js:L290-295`: Thiếu validation `if (quantity <= 0)`.""",
        "labels": ["bug", "FR-07", "severity:high"]
    },
    {
        "id": "BUG-FR07-02",
        "title": "[BUG-FR07-02] Thêm sản phẩm số lượng = 0 vẫn được server chấp nhận",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-02`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `POST /api/cart`
- **Mức độ nghiêm trọng:** Medium
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Gửi request thêm sản phẩm với `quantity = 0` được server chấp nhận trả về `200 OK` thay vì từ chối `400 Bad Request`.""",
        "labels": ["bug", "FR-07", "severity:medium"]
    },
    {
        "id": "BUG-FR07-03",
        "title": "[BUG-FR07-03] Thiếu hoàn toàn API Cập nhật số lượng giỏ hàng (PUT /api/cart)",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-03`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `PUT /api/cart`
- **Mức độ nghiêm trọng:** **Critical** (Missing Feature)
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Đặc tả SRS yêu cầu API cập nhật số lượng item trong giỏ hàng (`PUT /api/cart`), nhưng backend hoàn toàn chưa cài đặt route này. Client gọi đến nhận mã lỗi `404 Not Found`.""",
        "labels": ["bug", "FR-07", "severity:critical"]
    },
    {
        "id": "BUG-FR07-04",
        "title": "[BUG-FR07-04] Thiếu hoàn toàn API Xóa item khỏi giỏ hàng (DELETE /api/cart/:id)",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR07-04`
- **Phân hệ:** Pool B (FR-07: Giỏ hàng)
- **API Endpoint:** `DELETE /api/cart/:id`
- **Mức độ nghiêm trọng:** **Critical** (Missing Feature)
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Đặc tả SRS yêu cầu endpoint xóa sản phẩm khỏi giỏ hàng, nhưng route `DELETE /api/cart/:id` hoàn toàn vắng mặt trong backend, trả về `404 Not Found`.""",
        "labels": ["bug", "FR-07", "severity:critical"]
    },
    {
        "id": "BUG-FR15-01",
        "title": "[BUG-FR15-01] Lỗ hổng bảo mật SEC-03: Thiếu middleware xác thực Admin (authenticateToken) trên CRUD sản phẩm",
        "body": """### 📌 Thông tin lỗi (Security Defect Metadata)
- **Mã lỗi:** `BUG-FR15-01` (OWASP API Security `SEC-03` - Broken Function Level Authorization)
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `POST/PUT/DELETE /api/products`
- **Mức độ nghiêm trọng:** **Critical**
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 🚨 Mô tả lỗ hổng bảo mật
Các endpoint tạo, sửa, xóa sản phẩm hoàn toàn không gắn middleware `authenticateToken`. Bất kỳ ai không cần đăng nhập hay truyền Token Authorization nào cũng có thể thêm/sửa/xóa sản phẩm trong hệ thống.

### 🧑‍💻 Vị trí mã nguồn
Tại `server.js:L167, 179, 191`:
```javascript
// Lỗi hiện tại:
app.post("/api/products", (req, res) => { ... });
app.put("/api/products/:id", (req, res) => { ... });
app.delete("/api/products/:id", (req, res) => { ... });

// Đề xuất sửa:
app.post("/api/products", authenticateToken, (req, res) => { ... });
app.put("/api/products/:id", authenticateToken, (req, res) => { ... });
app.delete("/api/products/:id", authenticateToken, (req, res) => { ... });
```""",
        "labels": ["bug", "security", "FR-15", "severity:critical"]
    },
    {
        "id": "BUG-FR15-02",
        "title": "[BUG-FR15-02] Ép kiểu price sang String ở các sản phẩm có ID chẵn",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR15-02`
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `GET /api/products/:id`
- **Mức độ nghiêm trọng:** Medium
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Khi lấy chi tiết sản phẩm có ID chẵn (ví dụ `id: 2`), trường `price` bị ép kiểu sang chuỗi String (`"price": "28000000"`) thay vì kiểu số Number (`28000000`), vi phạm đặc tả OpenAPI/JSON Schema.

### 🧑‍💻 Nguyên nhân gốc
Tại `server.js:L162`:
```javascript
if (row.id % 2 === 0) {
    row.price = String(row.price); // Lỗi ép kiểu
}
```""",
        "labels": ["bug", "FR-15", "severity:medium"]
    },
    {
        "id": "BUG-FR15-03",
        "title": "[BUG-FR15-03] Cho phép tạo sản phẩm với giá âm (price < 0)",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR15-03`
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `POST /api/products`
- **Mức độ nghiêm trọng:** High
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Tạo sản phẩm với `price: -500000` được server chấp nhận trả về `200 OK` thay vì từ chối `400 Bad Request`.""",
        "labels": ["bug", "FR-15", "severity:high"]
    },
    {
        "id": "BUG-FR15-04",
        "title": "[BUG-FR15-04] Xóa/Sửa sản phẩm không cần quyền Admin",
        "body": """### 📌 Thông tin lỗi (Defect Metadata)
- **Mã lỗi:** `BUG-FR15-04`
- **Phân hệ:** Pool C (FR-15: Quản lý sản phẩm)
- **API Endpoint:** `DELETE /api/products/:id`
- **Mức độ nghiêm trọng:** **Critical**
- **Sinh viên báo cáo:** Lâm Hữu Khánh (`23127205`)

### 📝 Mô tả lỗi
Bất kỳ request `DELETE /api/products/:id` nào gửi lên mà không có Token Authorization hoặc chỉ là User thường đều xóa được sản phẩm trong CSDL SQLite.""",
        "labels": ["bug", "security", "FR-15", "severity:critical"]
    }
]


def post_issue(token: str, issue_data: dict) -> dict:
    payload = json.dumps({
        "title": issue_data["title"],
        "body": issue_data["body"],
        "labels": issue_data["labels"]
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "HW06-API-Testing-Script"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[-] HTTP {e.code} Error: {err_msg}")
        return None
    except Exception as e:
        print(f"[-] Exception: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Publish 12 Bug Reports to GitHub Issues")
    parser.add_argument("--token", "-t", required=True, help="GitHub Personal Access Token")
    args = parser.parse_args()

    print("=" * 70)
    print(f"  PUBLISHING 12 BUG REPORTS TO GITHUB: {REPO_OWNER}/{REPO_NAME}")
    print("=" * 70)

    success_count = 0
    for idx, item in enumerate(ISSUES_DATA, start=1):
        print(f"\n[{idx}/12] Posting: {item['id']} - {item['title'][:45]}...")
        res = post_issue(args.token, item)
        if res:
            issue_number = res.get("number")
            issue_url = res.get("html_url")
            print(f"    [+] Created Issue #{issue_number}: {issue_url}")
            success_count += 1
        else:
            print(f"    [-] Failed to post {item['id']}")

        time.sleep(1)  # Rate-limit safety

    print("\n" + "=" * 70)
    print(f"  SUMMARY: Successfully posted {success_count}/12 issues to GitHub!")
    print("=" * 70)


if __name__ == "__main__":
    main()
