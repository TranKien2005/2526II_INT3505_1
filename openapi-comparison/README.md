# So sánh các chuẩn tài liệu hóa API

Dự án demo cách tài liệu hóa API Quản lý Thư viện bằng 4 format phổ biến: **OpenAPI**, **API Blueprint**, **RAML**, và **TypeSpec**.

| Tiêu chí | OpenAPI (Swagger) | API Blueprint | RAML | TypeSpec |
| --- | --- | --- | --- | --- |
| **Định dạng** | YAML / JSON | Markdown | YAML | Ngôn ngữ riêng (Type-safe) |
| **Tính dễ đọc** | Trung bình (Dài dòng) | Rất cao (Markdown) | Cao | Rất cao (Giống TypeScript) |
| **Hệ sinh thái/Công cụ** | Cực kỳ phong phú (Chuẩn công nghiệp) | Ít công cụ, không cập nhật nhiều | Ít cập nhật | Mới, của Microsoft, đang phát triển nhanh |
| **Khả năng tái sử dụng** | `$ref` | Data Structures (MSON) | Traits, Resource Types | Tái sử dụng tốt nhờ function, tính kế thừa |
| **Sinh Code/Test** | OpenAPIGenerator, Schemathesis | Dredd | osprey | Tự động biên dịch ra OpenAPI sau đó dùng tool OpenAPI |

---

## Ứng dụng quản lý Thư Viện (Demo)

Mỗi thư mục con tương ứng một format tài liệu hóa để mô tả API cơ bản của một ứng dụng quản lý sách, bao gồm:
- Lấy danh sách sách: `GET /books`
- Thêm sách mới: `POST /books`
- Lấy thông tin chi tiết một cuốn sách: `GET /books/{id}`
- Xóa sách: `DELETE /books/{id}`

Tham khảo `README.md` bên trong từng thư mục để biết cách viết, cách tải công cụ xem (viewer) và cách sinh code/test từ mỗi định dạng.
