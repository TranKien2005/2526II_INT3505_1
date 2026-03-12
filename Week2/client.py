import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_get_users():
    print_separator("1. GET - Lấy danh sách người dùng")
    response = requests.get(f"{BASE_URL}/api/v1/users?page=1&limit=2")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_update_email_not_found():
    print_separator("2.1. PATCH - Cập nhật email (Test Lỗi 404 - Không tồn tại)")
    payload = {"email": "test@example.com"}
    response = requests.patch(f"{BASE_URL}/api/v1/users/999/email", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_update_email_invalid():
    print_separator("2.2. PATCH - Cập nhật email (Test Lỗi 422 - Sai định dạng Email)")
    payload = {"email": "dia_chi_email_sai"}
    response = requests.patch(f"{BASE_URL}/api/v1/users/123/email", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_update_email_success():
    print_separator("2.3. PATCH - Cập nhật email (Thành công đổi email)")
    payload = {"email": "new_email@example.com"}
    response = requests.patch(f"{BASE_URL}/api/v1/users/123/email", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_create_post_success():
    print_separator("3.1 POST - Tạo bài viết mới (Thành công)")
    payload = {
        "title": "Hướng dẫn API HTTP",
        "content": "Nội dung chi tiết về các lỗi HTTP...",
        "author_id": 123
    }
    response = requests.post(f"{BASE_URL}/api/v1/posts", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_create_post_server_error():
    print_separator("3.2 POST - Tạo bài viết mới (Test Lỗi 500 - Gửi 'error' trong title)")
    payload = {
        "title": "error",
        "content": "Gây lỗi server",
        "author_id": 123
    }
    response = requests.post(f"{BASE_URL}/api/v1/posts", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_delete_comment_forbidden():
    print_separator("4.1 DELETE - Xóa bình luận (Test Lỗi 403 - User không có quyền)")
    response = requests.delete(f"{BASE_URL}/api/v1/comments/456?user_role=user")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print("Response: <No Content>")

def test_delete_comment_success():
    print_separator("4.2 DELETE - Xóa bình luận (Thành công với role admin)")
    response = requests.delete(f"{BASE_URL}/api/v1/comments/456?user_role=admin")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Response: <204 No Content - Đã xóa thành công>")
    else:
        print(f"Response: {response.json()}")

def test_upload_avatar_invalid_type():
    print_separator("5.1 POST - Upload Avatar (Test Lỗi 400 - File PDF không hợp lệ)")
    files = {
        'avatar': ('document.pdf', b'dummy pdf content', 'application/pdf')
    }
    response = requests.post(f"{BASE_URL}/api/v1/users/123/avatar", files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_upload_avatar_success():
    print_separator("5.2 POST - Upload Avatar (Thành công với ảnh)")
    files = {
        'avatar': ('my_photo.jpg', b'dummy image content', 'image/jpeg')
    }
    response = requests.post(f"{BASE_URL}/api/v1/users/123/avatar", files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("Bắt đầu test API client...")
    
    # Kiểm tra xem server FastAPI đã bật chưa
    try:
        requests.get(f"{BASE_URL}/docs")
    except requests.exceptions.ConnectionError:
        print("LỖI: Không kết nối được với Server FastAPI!")
        print("=> Hãy mở 1 Terminal khác và chạy: 'uvicorn server:app --reload'")
        sys.exit(1)

    # Chạy tuần tự các kịch bản test
    test_get_users()
    
    test_update_email_not_found()
    test_update_email_invalid()
    test_update_email_success()
    
    test_create_post_success()
    test_create_post_server_error()
    
    test_delete_comment_forbidden()
    test_delete_comment_success()
    
    test_upload_avatar_invalid_type()
    test_upload_avatar_success()
    
    print_separator("Test hoàn thành!")
