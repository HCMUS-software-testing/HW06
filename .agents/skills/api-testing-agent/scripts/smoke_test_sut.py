#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: SUT Backend Pre-flight Smoke Tester
Author: Lam Huu Khanh (Student ID: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing

Description:
  Quickly verifies functional availability of the 3 target API pools:
  - Pool A: POST /api/login (FR-02)
  - Pool B: GET / POST /api/cart (FR-07)
  - Pool C: GET / POST /api/products (FR-15)
=============================================================================
"""

import sys
import json
import urllib.request
import urllib.error

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_URL = "http://localhost:3000"


def send_http(endpoint: str, method: str = "GET", headers: dict = None, data: dict = None):
    url = f"{BASE_URL}{endpoint}"
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    body_bytes = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body_bytes, headers=req_headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body_text = resp.read().decode("utf-8")
            try:
                body_json = json.loads(body_text)
            except Exception:
                body_json = body_text
            return status, body_json
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            body_json = json.loads(err_body)
        except Exception:
            body_json = err_body
        return e.code, body_json
    except Exception as e:
        return 0, str(e)


def run_smoke_test():
    print("=" * 60)
    print("  HW06 SUT BACKEND PRE-FLIGHT SMOKE TEST (PORT 3000)")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    # 1. Test FR-02: POST /api/login
    print("\n[1/3] Testing Pool A: FR-02 Login (POST /api/login)...")
    login_body = {"email": "test@eshop.com", "password": "Test1234!"}
    status, res = send_http("/api/login", method="POST", data=login_body)
    if status == 200 and isinstance(res, dict) and "token" in res:
        user_token = res["token"]
        print(f"  ✅ [PASS] HTTP 200 OK | Token: {user_token[:28]}...")
    else:
        print(f"  ❌ [FAIL] HTTP {status} | Error: {res}")
        print("  [!] Please ensure SUT backend is running: cd eshop-sut/backend && node server.js")
        return False

    auth_header = {"Authorization": f"Bearer {user_token}"}

    # 2. Test FR-07: GET & POST /api/cart
    print("\n[2/3] Testing Pool B: FR-07 Cart (GET & POST /api/cart)...")
    status_get, res_get = send_http("/api/cart", method="GET", headers=auth_header)
    print(f"  - GET /api/cart: HTTP {status_get} | Items count: {len(res_get) if isinstance(res_get, list) else 'N/A'}")

    cart_item = {"id": 1, "name": "iPhone 15", "price": 30000000, "quantity": 1}
    status_post, res_post = send_http("/api/cart", method="POST", headers=auth_header, data=cart_item)
    if status_post == 200:
        print(f"  ✅ [PASS] POST /api/cart: HTTP 200 OK | {res_post}")
    else:
        print(f"  ❌ [FAIL] POST /api/cart: HTTP {status_post} | {res_post}")
        return False

    # 3. Test FR-15: GET & POST /api/products
    print("\n[3/3] Testing Pool C: FR-15 Product CRUD (GET /api/products)...")
    status_prod, res_prod = send_http("/api/products", method="GET")
    if status_prod == 200 and isinstance(res_prod, list) and len(res_prod) > 0:
        print(f"  ✅ [PASS] GET /api/products: HTTP 200 OK | Total products: {len(res_prod)}")
        print(f"    Sample Product: ID {res_prod[0].get('id')} - {res_prod[0].get('name')} ({res_prod[0].get('price')} VND)")
    else:
        print(f"  ❌ [FAIL] GET /api/products: HTTP {status_prod} | {res_prod}")
        return False

    print("\n" + "=" * 60)
    print("  [RESULT] All 3 Target API Pools are UP and RESPONDING!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)
