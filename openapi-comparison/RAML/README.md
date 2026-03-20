# RAML Demo

Thư mục này chứa định nghĩa API bằng ngôn ngữ RAML (RESTful API Modeling Language).

## 1. Cài đặt và Chạy (Viewer)
Cài đặt `raml2html` để chuyển đổi file RAML thành một trang tài liệu HTML:

```bash
# Cài đặt raml2html global
npm i -g raml2html

# Build file html
raml2html api.raml > api.html
```
Sau đó bạn có thể mở `api.html` bằng trình duyệt web để xem tài liệu chi tiết.

## 2. Demo Sinh Code / Mock API
Sử dụng `osprey-mock-service` để tạo một mock server trực tiếp từ file RAML định nghĩa.

```bash
# Cài đặt công cụ osprey mock
npm install -g osprey-mock-service

# Khởi chạy mock dựa tên file tài liệu
osprey-mock-service -f api.raml -p 3000
```
Sau khi chạy, API của bạn đã có thể được gọi tại `http://localhost:3000/books`.

Để sinh code thực sự, bạn có thể dùng `raml-generator`, tuy nhiên hệ sinh thái RAML hiện nay không còn được cập nhật mạnh mẽ cho phần sinh mã nguồn như hệ sinh thái OpenAPI.
