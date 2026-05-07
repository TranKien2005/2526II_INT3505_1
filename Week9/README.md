# Thực hành: Chiến lược nâng cấp API

Thư mục này chứa nội dung thực hành cho việc thiết kế chiến lược nâng cấp API từ v1 sang v2.

## Các tệp tin:
1. **`main_v1.py`**: Mã nguồn API Thanh toán phiên bản 1 (Sử dụng FastAPI).
2. **`STRATEGY_AND_DEPRECATION.md`**: Tài liệu thiết kế chiến lược nâng cấp và mẫu thông báo Deprecation gửi cho các Developer.

## Cách chạy API v2:
Lưu ý: v2 hỗ trợ cả các endpoint cũ (có cảnh báo) và endpoint mới.

```powershell
# Chạy v2 trên cổng 8001 để tránh xung đột với v1
.\.vevn\Scripts\python.exe .\Week9\main_v2.py
```

## Các điểm khác biệt quan trọng trong v2:
1. **URL Versioning**: Truy cập qua `/v1/...` (Legacy) hoặc `/v2/...` (Modern).
2. **Security**: Không còn dùng `card_number`, thay bằng `payment_method_id`.
3. **Deprecation Header**: Nếu bạn gọi `/v1/payments`, hãy kiểm tra tab **Headers** trong response, bạn sẽ thấy:
   `Warning: 299 - "v1 is deprecated..."`
4. **Data Mapping**: v2 có khả năng đọc và chuyển đổi dữ liệu cũ từ v1 sang định dạng mới.

## Thử thách:
Hãy thử dùng Postman hoặc curl để gọi `POST http://127.0.0.1:8001/v1/payments` và quan sát header trả về. Sau đó thử dùng `/v2/payments` để thấy sự khác biệt về cấu trúc JSON.
