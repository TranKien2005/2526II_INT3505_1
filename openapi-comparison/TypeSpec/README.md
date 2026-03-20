# TypeSpec Demo (trước đây là CADL của Microsoft)

TypeSpec là ngôn ngữ mô tả API mới, sử dụng syntax gần tương đồng với TypeScript thay vì JSON hay YAML, giúp cho việc viết đặc tả trở nên rõ ràng và ít bị lặp code hơn.

## 1. Cài đặt
Cần cài đặt Node.js trước đó. Khởi tạo và cài các module TypeSpec:

```bash
# Cài compiler global
npm install -g @typespec/compiler

# Tại thư mục TypeSpec, khởi tạo node project nếu cần
# npm init -y

# Cài library http và openapi3 cho TypeSpec
npm install @typespec/http @typespec/openapi3
```

## 2. Biên dịch & Xem tài liệu (Viewer)
Mặc định TypeSpec không có UI riêng, mà định hướng biên dịch ra OpenAPI sau đó dùng hệ sinh thái OpenAPI.

Biên dịch TypeSpec thành OpenAPI:
```bash
tsp compile main.tsp --emit @typespec/openapi3
```
Lệnh này sẽ tạo ra file `openapi.yaml` (nằm trong thư mục `tsp-output/`). Bạn có thể sử dụng Swagger UI (như hướng dẫn trong thư mục OpenAPI) để mở và đọc cấu trúc API.

## 3. Demo Sinh Code / Sinh Test
Khi file TypeSpec đã được compile ra thành `openapi.yaml`, việc sinh code hoàn toàn giống bên OpenAPI. Bạn có thể sử dụng **OpenAPI Generator** hoặc **Kiota** trên tệp YAML vừa lấy.

Ví dụ:
```bash
npx @openapitools/openapi-generator-cli generate -i ./tsp-output/openapi.yaml -g fastapi -o ./generated-code
```
