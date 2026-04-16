Bước 1: Chuyển đổi API Blueprint sang OpenAPI
Bạn cần công cụ apib2swagger (yêu cầu cài đặt Node.js).
Cài đặt apib2swagger qua npm (nếu chưa có):
npm install -g apib2swagger
Chạy lệnh để chuyển đổi file .apib của bạn thành file .yaml (chuẩn OpenAPI 3.0):
apib2swagger -i your_api_file.apib -o swagger_api.yaml --openapi
Bước 2: Sinh ra mã nguồn Python từ file OpenAPI
Bạn sẽ sử dụng openapi-generator-cli (cũng có thể cài qua npm hoặc chạy file .jar, hoặc qua Docker).
Cài đặt openapi-generator-cli qua npm:
A. Sinh code cho Client (Nơi gọi API) Ví dụ bạn muốn sinh ra một SDK Python để ứng dụng khác có thể gọi API của bạn dễ dàng:
openapi-generator-cli generate -i swagger_api.yaml -g python -o ./python-client
B. Sinh code cho Server (Nơi cung cấp API) Nếu bạn muốn tạo khung sườn (skeleton/stub) để code backend, bạn có thể chọn framework như python-fastapi hoặc python-flask:
openapi-generator-cli generate -i swagger_api.yaml -g python-fastapi -o ./python-server
