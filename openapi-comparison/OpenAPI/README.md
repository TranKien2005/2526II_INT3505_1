# OpenAPI Demo

Đây là thư mục chứa định nghĩa API bằng OpenAPI.

## 1. Cài đặt và Chạy (Viewer)
Có thể sử dụng **Swagger UI** để xem tài liệu một cách trực quan:

```bash
# Cài đặt swagger-ui-watcher
npm install -g swagger-ui-watcher

# Chạy viewer
swagger-ui-watcher openapi.yaml
```

## 2. Demo Sinh Code
Sử dụng **OpenAPI Generator** để sinh code server/client.

Ví dụ sinh mã nguồn Python FastAPI (Server):
```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g fastapi -o ./generated-code
```

Ví dụ sinh mã nguồn TypeScript Axios (Client):
```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ./generated-client
```

## 3. Demo Sinh Test
Sử dụng công cụ **Schemathesis** để tự động sinh test case dựa theo schema.
```bash
# Cài đặt schemathesis
pip install schemathesis

# Chạy test vào một API đang host ở localhost:8000
schemathesis run openapi.yaml --base-url http://localhost:8000
```

npm install @openapitools/openapi-generator-cli

npx openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server

  A. Client (frontend / gọi API)
Generator	Dùng cho
typescript-axios	React, Vue, Angular
typescript-fetch	Web thuần
javascript	JS cơ bản
java	Java client
python	Python client

B. Server (backend)
Generator	Framework
nodejs-express-server	Node.js (Express)
python-fastapi	FastAPI
spring	Spring Boot (Java)
go-server	Golang
aspnetcore	.NET