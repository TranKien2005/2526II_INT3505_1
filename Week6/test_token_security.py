"""
Script kiểm tra bảo mật token JWT cho Week6 API.
Các test case:
1. Truy cập endpoint bảo vệ mà KHÔNG có token
2. Truy cập với token sai / giả mạo
3. Truy cập với token hết hạn
4. Kiểm tra response headers có lộ token không
5. Kiểm tra error messages có lộ thông tin nhạy cảm không
6. Kiểm tra token không xuất hiện trong response body khi gọi /books
7. Kiểm tra login sai password không lộ thông tin
8. Kiểm tra token có chứa password không (decode payload)
"""

import requests
import jwt
import json
from datetime import datetime, timedelta, timezone

BASE = "http://127.0.0.1:8000"
SECRET_KEY = "my-super-secret-key-change-in-production"

PASS_COUNT = 0
FAIL_COUNT = 0
WARN_COUNT = 0


def result(test_name, passed, detail="", warn=False):
    global PASS_COUNT, FAIL_COUNT, WARN_COUNT
    if warn:
        WARN_COUNT += 1
        icon = "⚠️  WARN"
    elif passed:
        PASS_COUNT += 1
        icon = "✅ PASS"
    else:
        FAIL_COUNT += 1
        icon = "❌ FAIL"
    print(f"{icon}  | {test_name}")
    if detail:
        print(f"         └─ {detail}")


print("=" * 65)
print("  🔐  KIỂM TRA BẢO MẬT TOKEN JWT - Week6 API")
print("=" * 65)

# ── Setup: đăng ký + đăng nhập ──
USERNAME = "sectest_user"
PASSWORD = "sectest_pass123"

r = requests.post(f"{BASE}/auth/register", json={"username": USERNAME, "password": PASSWORD})
if r.status_code not in (201, 400):  # 400 = already exists
    print(f"❌ Không thể đăng ký user test. Status: {r.status_code}")
    exit(1)

r = requests.post(f"{BASE}/auth/login", data={"username": USERNAME, "password": PASSWORD})
if r.status_code != 200:
    print(f"❌ Không thể đăng nhập. Status: {r.status_code}")
    exit(1)

VALID_TOKEN = r.json()["access_token"]
print(f"\n📌 Đã lấy được token hợp lệ (dài {len(VALID_TOKEN)} ký tự)\n")
print("-" * 65)

# ══════════════════════════════════════════════════════════════
# TEST 1: Truy cập /books KHÔNG có token
# ══════════════════════════════════════════════════════════════
r = requests.get(f"{BASE}/books")
result(
    "Truy cập /books không có token → bị chặn (401)",
    r.status_code == 401,
    f"Status: {r.status_code}",
)

# ══════════════════════════════════════════════════════════════
# TEST 2: Response 401 KHÔNG lộ thông tin server/token
# ══════════════════════════════════════════════════════════════
body_str = r.text.lower()
leaked_info = []
for keyword in ["secret", "key", "password", "hash", "bcrypt", "algorithm", "hs256"]:
    if keyword in body_str:
        leaked_info.append(keyword)

result(
    "Response 401 không lộ thông tin nhạy cảm",
    len(leaked_info) == 0,
    f"Từ khóa bị lộ: {leaked_info}" if leaked_info else "Không tìm thấy từ khóa nhạy cảm",
)

# ══════════════════════════════════════════════════════════════
# TEST 3: Dùng token giả mạo (fake secret key)
# ══════════════════════════════════════════════════════════════
fake_token = jwt.encode(
    {"sub": USERNAME, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
    "FAKE-SECRET-KEY",
    algorithm="HS256",
)
r = requests.get(f"{BASE}/books", headers={"Authorization": f"Bearer {fake_token}"})
result(
    "Token giả mạo (sai secret) → bị chặn (401)",
    r.status_code == 401,
    f"Status: {r.status_code}",
)

# ══════════════════════════════════════════════════════════════
# TEST 4: Dùng token hết hạn
# ══════════════════════════════════════════════════════════════
expired_token = jwt.encode(
    {"sub": USERNAME, "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
    SECRET_KEY,
    algorithm="HS256",
)
r = requests.get(f"{BASE}/books", headers={"Authorization": f"Bearer {expired_token}"})
result(
    "Token hết hạn → bị chặn (401)",
    r.status_code == 401,
    f"Status: {r.status_code}, Detail: {r.json().get('detail', '')}",
)

# ══════════════════════════════════════════════════════════════
# TEST 5: Token không chứa 'sub' claim
# ══════════════════════════════════════════════════════════════
no_sub_token = jwt.encode(
    {"data": "random", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
    SECRET_KEY,
    algorithm="HS256",
)
r = requests.get(f"{BASE}/books", headers={"Authorization": f"Bearer {no_sub_token}"})
result(
    "Token không có 'sub' claim → bị chặn (401)",
    r.status_code == 401,
    f"Status: {r.status_code}",
)

# ══════════════════════════════════════════════════════════════
# TEST 6: Response headers không lộ token
# ══════════════════════════════════════════════════════════════
r = requests.get(f"{BASE}/books", headers={"Authorization": f"Bearer {VALID_TOKEN}"})
headers_str = str(r.headers).lower()
token_in_headers = VALID_TOKEN.lower() in headers_str

result(
    "Response headers không chứa token",
    not token_in_headers,
    "Token bị lộ trong response headers!" if token_in_headers else "OK",
)

# ══════════════════════════════════════════════════════════════
# TEST 7: Response body /books không chứa token
# ══════════════════════════════════════════════════════════════
body_str = r.text
token_in_body = VALID_TOKEN in body_str

result(
    "Response body /books không chứa token",
    not token_in_body,
    "Token bị lộ trong response body!" if token_in_body else "OK",
)

# ══════════════════════════════════════════════════════════════
# TEST 8: Login sai password không lộ thông tin user
# ══════════════════════════════════════════════════════════════
r = requests.post(f"{BASE}/auth/login", data={"username": USERNAME, "password": "wrong_pass"})
result(
    "Login sai password → 401 và không lộ thông tin",
    r.status_code == 401,
    f"Detail: {r.json().get('detail', '')}",
)
# Check response doesn't reveal whether username exists
detail = r.json().get("detail", "").lower()
reveals_username = "không tồn tại" in detail or "not found" in detail or "user" in detail.replace("username", "")
result(
    "Error message không phân biệt sai user/sai pass",
    not reveals_username,
    f"Message: '{r.json().get('detail', '')}'",
)

# ══════════════════════════════════════════════════════════════
# TEST 9: Token payload KHÔNG chứa password
# ══════════════════════════════════════════════════════════════
decoded = jwt.decode(VALID_TOKEN, SECRET_KEY, algorithms=["HS256"])
has_password = any(
    k in decoded for k in ["password", "pass", "hashed_password", "pwd"]
)
result(
    "Token payload không chứa password",
    not has_password,
    f"Payload keys: {list(decoded.keys())}",
)

# ══════════════════════════════════════════════════════════════
# TEST 10: Token dùng chuỗi ngẫu nhiên (garbage)
# ══════════════════════════════════════════════════════════════
r = requests.get(f"{BASE}/books", headers={"Authorization": "Bearer aaa.bbb.ccc"})
result(
    "Token rác (garbage string) → bị chặn (401)",
    r.status_code == 401,
    f"Status: {r.status_code}",
)

# ══════════════════════════════════════════════════════════════
# TEST 11: Không có header Authorization
# ══════════════════════════════════════════════════════════════
r = requests.get(f"{BASE}/books", headers={})
result(
    "Không có Authorization header → bị chặn (401)",
    r.status_code == 401,
    f"Status: {r.status_code}",
)

# ══════════════════════════════════════════════════════════════
# TEST 12: Kiểm tra SECRET_KEY không lộ qua /docs hoặc /openapi.json
# ══════════════════════════════════════════════════════════════
r = requests.get(f"{BASE}/openapi.json")
openapi_str = r.text.lower()
secret_in_docs = SECRET_KEY.lower() in openapi_str or "secret" in openapi_str

result(
    "OpenAPI spec không chứa secret key",
    SECRET_KEY.lower() not in openapi_str,
    "Secret key bị lộ trong /openapi.json!" if SECRET_KEY.lower() in openapi_str else "OK",
)

# ══════════════════════════════════════════════════════════════
# TEST 13: POST /books với token hợp lệ → hoạt động bình thường
# ══════════════════════════════════════════════════════════════
r = requests.post(
    f"{BASE}/books",
    json={"title": "Test Book", "author": "Tester"},
    headers={"Authorization": f"Bearer {VALID_TOKEN}"},
)
result(
    "POST /books với token hợp lệ → 201",
    r.status_code == 201,
    f"Status: {r.status_code}",
)
# Check response doesn't leak token
if r.status_code == 201:
    result(
        "Response tạo sách không chứa token",
        VALID_TOKEN not in r.text,
        "OK" if VALID_TOKEN not in r.text else "Token lộ trong response!",
    )

# ══════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print(f"  📊 KẾT QUẢ: ✅ {PASS_COUNT} passed | ❌ {FAIL_COUNT} failed | ⚠️  {WARN_COUNT} warnings")
total = PASS_COUNT + FAIL_COUNT
if FAIL_COUNT == 0:
    print("  🎉 Tất cả test đều PASS! API không bị lộ token.")
else:
    print(f"  ⚠️  Có {FAIL_COUNT}/{total} test FAIL — cần kiểm tra lại!")
print("=" * 65)
