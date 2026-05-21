# Week 11 - API Design Patterns Demo

Dự án cực kỳ đơn giản dùng **FastAPI**. Mỗi mẫu thiết kế API nằm trong **một file riêng** để dễ demo và dễ chỉ ra sự khác biệt.

## Các file chính

| File | Mẫu thiết kế | Ý nghĩa |
|---|---|---|
| `crud_api.py` | CRUD | Tạo, đọc, sửa, xóa notification |
| `query_api.py` | Query | Lọc danh sách notification bằng query parameters |
| `hateoas_api.py` | HATEOAS | Response có thêm `links` để client biết hành động tiếp theo |
| `event_api.py` | Event-driven | Khi tạo notification thì phát event nội bộ ra terminal |
| `webhook_api.py` | Webhook | Khi tạo notification thì gọi sang server khác qua HTTP |
| `webhook_receiver.py` | Webhook receiver | Server giả lập hệ thống bên ngoài nhận webhook |

Dữ liệu chỉ lưu tạm trong memory bằng list Python, không dùng database.

---

# 1. Cài đặt

Mở terminal tại folder `Week11`.

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nếu chưa có môi trường ảo:

```powershell
python -m venv .venv
```

---

# 2. Demo CRUD pattern

Chạy server:

```powershell
uvicorn crud_api:app --reload --port 8001
```

Mở Swagger:

```text
http://localhost:8001/docs
```

CRUD có 5 endpoint:

```http
POST /notifications
GET /notifications
GET /notifications/{notification_id}
PUT /notifications/{notification_id}
DELETE /notifications/{notification_id}
```

Body mẫu khi tạo:

```json
{
  "title": "Welcome",
  "message": "Hello user"
}
```

## Điểm cần nói

CRUD dùng khi tài nguyên có vòng đời rõ ràng: tạo, xem, sửa, xóa.

---

# 3. Demo Query pattern

Chạy server:

```powershell
uvicorn query_api:app --reload --port 8002
```

Mở Swagger:

```text
http://localhost:8002/docs
```

Endpoint chính:

```http
GET /notifications
```

Demo lọc theo query parameters:

```http
GET /notifications?type=email
GET /notifications?status=sent
GET /notifications?type=email&status=sent
```

## Điểm khác CRUD

CRUD là thao tác trực tiếp với tài nguyên. Query là tìm kiếm hoặc lọc danh sách tài nguyên.

---

# 4. Demo HATEOAS pattern

Chạy server:

```powershell
uvicorn hateoas_api:app --reload --port 8003
```

Mở Swagger:

```text
http://localhost:8003/docs
```

Gọi:

```http
GET /notifications
GET /notifications/1
```

Response có thêm `links`:

```json
{
  "id": 1,
  "title": "Welcome",
  "message": "Hello user",
  "links": {
    "self": "/notifications/1",
    "all": "/notifications",
    "delete": "/notifications/1"
  }
}
```

## Điểm khác CRUD

CRUD chỉ có endpoint. HATEOAS làm response có thêm link để client biết có thể gọi API nào tiếp theo.

---

# 5. Demo Event-driven pattern

Chạy server:

```powershell
uvicorn event_api:app --reload --port 8004
```

Mở Swagger:

```text
http://localhost:8004/docs
```

Gọi:

```http
POST /notifications
```

Body:

```json
{
  "title": "Event demo",
  "message": "Create notification and publish event"
}
```

Quan sát terminal đang chạy server, sẽ thấy:

```text
EVENT: notification.created
DATA: {...}
```

## Điểm khác CRUD

CRUD là client gọi API để xử lý dữ liệu. Event-driven là hệ thống tự phát sự kiện khi có hành động xảy ra.

---

# 6. Demo Webhook pattern

Webhook demo có 2 server:

- Server nhận webhook: `webhook_receiver.py`, port `4000`
- Server gửi webhook: `webhook_api.py`, port `8005`

Trong file `webhook_api.py`, URL webhook đã được hardcode:

```text
http://localhost:4000/webhook
```

Vì vậy khi demo **không cần nhập URL webhook**.

## Bước 1: Chạy webhook receiver

Terminal 1:

```powershell
uvicorn webhook_receiver:app --reload --port 4000
```

## Bước 2: Chạy webhook API

Terminal 2:

```powershell
uvicorn webhook_api:app --reload --port 8005
```

Mở Swagger của webhook API:

```text
http://localhost:8005/docs
```

## Bước 3: Tạo notification

Gọi:

```http
POST /notifications
```

Body:

```json
{
  "title": "Webhook demo",
  "message": "Create notification and call another server"
}
```

## Bước 4: Quan sát kết quả

Terminal của `webhook_receiver.py` sẽ in ra:

```text
WEBHOOK RECEIVED: {'event': 'notification.created', 'data': {...}}
```

## Điểm khác Event-driven

Event-driven chỉ cần phát event trong hệ thống. Webhook là gửi event đó sang hệ thống khác bằng HTTP.

---

# 7. REST vs gRPC vs GraphQL

## REST

Demo này dùng REST vì:

- Dễ hiểu
- Dễ test bằng Swagger hoặc Postman
- Phù hợp CRUD và tài nguyên như `notifications`
- Dùng HTTP method rõ ràng: `GET`, `POST`, `PUT`, `DELETE`

## gRPC

Nên dùng gRPC khi:

- Giao tiếp giữa các service nội bộ
- Cần tốc độ cao
- Cần contract chặt chẽ bằng file `.proto`

Ví dụ: notification service gọi user service trong backend lớn.

## GraphQL

Nên dùng GraphQL khi:

- Frontend cần lấy dữ liệu linh hoạt
- Client muốn chọn field cần lấy
- Một màn hình cần gom dữ liệu từ nhiều resource

Ví dụ: client chỉ muốn lấy `title` và `status`, không muốn lấy toàn bộ notification.

---

# 8. Thứ tự demo gợi ý

1. Chạy `crud_api.py` để demo CRUD.
2. Chạy `query_api.py` để demo Query.
3. Chạy `hateoas_api.py` để chỉ phần `links` trong response.
4. Chạy `event_api.py` rồi nhìn terminal để thấy event.
5. Chạy `webhook_receiver.py` và `webhook_api.py` để thấy webhook gọi sang server khác.
6. Kết luận: REST phù hợp demo này; gRPC và GraphQL phù hợp tình huống khác.
