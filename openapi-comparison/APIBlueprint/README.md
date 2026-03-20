# API Blueprint Demo

Thư mục này chứa định nghĩa API bằng API Blueprint.

## 1. Cài đặt và Chạy (Viewer)
Sử dụng **Aglio** để render file Blueprint thành HTML tĩnh:

```bash
# Cài đặt aglio
npm install -g aglio

# Build API docs sang HTML
aglio -i api.apib -o api.html
```
Sau đó bạn có thể mở tệp `api.html` trên trình duyệt để xem tài liệu cực kỳ đẹp mắt.

## 2. Demo Sinh Test (Dredd)
**Dredd** là một công cụ kiểm thử API sinh ra request thực tế cho backend server của bạn, thông qua việc đối chiếu với Blueprint.

```bash
# Cài đặt dredd
npm install -g dredd

# Chạy dredd (yêu cầu bạn có backend chạy ở 1 port cụ thể, ví dụ 8000)
dredd api.apib http://localhost:8000
```

## 3. Sinh Mock Server
Sử dụng **Drakov** để nhanh chóng dựng một server mock trả về dữ liệu mẫu có trong file `.apib`.

```bash
# Cài đặt drakov
npm install -g drakov

# Khởi chạy mock server ở port 3000
drakov -f api.apib -p 3000
```
