# Phân tích API của Stripe và GitHub theo API Design Patterns

Tài liệu này phân tích ngắn gọn các pattern xuất hiện trong API của **Stripe** và **GitHub**.

---

## 1. Stripe API

Stripe là nền tảng xử lý thanh toán. API của Stripe dùng nhiều pattern REST, CRUD, Query, Event-driven và Webhook.

### CRUD pattern

Stripe có nhiều tài nguyên như `customers`, `products`, `prices`, `payment_intents`.

Ví dụ:

```http
POST /v1/customers
GET /v1/customers/{id}
POST /v1/customers/{id}
DELETE /v1/customers/{id}
```

Ý nghĩa:

- Tạo customer mới
- Lấy thông tin customer
- Cập nhật customer
- Xóa customer

=> Đây là CRUD pattern vì API xoay quanh việc quản lý tài nguyên.

### Query pattern

Stripe cho phép lấy danh sách và lọc dữ liệu.

Ví dụ:

```http
GET /v1/payment_intents?customer=cus_xxx
GET /v1/charges?limit=10
```

Ý nghĩa:

- Lọc payment theo customer
- Giới hạn số bản ghi trả về

=> Đây là Query pattern vì client truyền điều kiện qua query parameters.

### Event-driven pattern

Stripe phát sinh event khi có hành động xảy ra.

Ví dụ:

```text
payment_intent.succeeded
invoice.paid
customer.created
charge.failed
```

Ý nghĩa:

- Thanh toán thành công
- Hóa đơn đã được thanh toán
- Customer mới được tạo
- Thanh toán thất bại

=> Đây là Event-driven vì hệ thống hoạt động dựa trên các sự kiện.

### Webhook pattern

Stripe dùng webhook để gửi event sang server của developer.

Ví dụ khi thanh toán thành công, Stripe gửi request:

```http
POST https://your-server.com/stripe-webhook
```

Body có dạng:

```json
{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_xxx",
      "status": "succeeded"
    }
  }
}
```

=> Đây là Webhook pattern vì Stripe chủ động gọi sang hệ thống bên ngoài khi có event.

### Kết luận về Stripe

Stripe dùng REST cho quản lý tài nguyên, Query cho lọc dữ liệu, Event-driven để mô hình hóa các thay đổi trong thanh toán, và Webhook để tích hợp với hệ thống bên ngoài.

---

## 2. GitHub API

GitHub là nền tảng quản lý source code. API của GitHub cũng sử dụng nhiều pattern như CRUD, Query, HATEOAS và Webhook.

### CRUD pattern

GitHub có các tài nguyên như `issues`, `pull requests`, `repositories`, `comments`.

Ví dụ với issue:

```http
POST /repos/{owner}/{repo}/issues
GET /repos/{owner}/{repo}/issues/{issue_number}
PATCH /repos/{owner}/{repo}/issues/{issue_number}
```

Ý nghĩa:

- Tạo issue
- Xem issue
- Cập nhật issue

=> Đây là CRUD pattern vì API thao tác trực tiếp với tài nguyên issue.

### Query pattern

GitHub cho phép lọc issue, pull request, commit theo nhiều điều kiện.

Ví dụ:

```http
GET /repos/{owner}/{repo}/issues?state=open
GET /repos/{owner}/{repo}/pulls?state=closed
GET /search/repositories?q=language:python
```

Ý nghĩa:

- Lọc issue đang mở
- Lọc pull request đã đóng
- Tìm repository theo ngôn ngữ Python

=> Đây là Query pattern vì API dùng query parameters để tìm kiếm/lọc dữ liệu.

### HATEOAS pattern

GitHub response thường có nhiều URL liên quan.

Ví dụ một issue có thể chứa:

```json
{
  "url": "https://api.github.com/repos/user/repo/issues/1",
  "comments_url": "https://api.github.com/repos/user/repo/issues/1/comments",
  "events_url": "https://api.github.com/repos/user/repo/issues/1/events",
  "html_url": "https://github.com/user/repo/issues/1"
}
```

Ý nghĩa:

- `url`: API lấy issue
- `comments_url`: API lấy comment của issue
- `events_url`: API lấy event của issue
- `html_url`: link xem trên trình duyệt

=> Đây là HATEOAS-like pattern vì response trả thêm link liên quan để client biết có thể truy cập tài nguyên nào tiếp theo.

### Event-driven pattern

GitHub có nhiều sự kiện xảy ra trong repository.

Ví dụ:

```text
push
pull_request
issues
issue_comment
release
workflow_run
```

Ý nghĩa:

- Có commit mới được push
- Pull request được mở hoặc cập nhật
- Issue được tạo hoặc sửa
- Có comment mới
- Có release mới
- GitHub Actions workflow chạy xong

=> Đây là Event-driven vì GitHub mô hình hóa hoạt động của repository thành các event.

### Webhook pattern

GitHub cho phép cấu hình webhook để gửi event sang server khác.

Ví dụ khi có push code, GitHub gửi request:

```http
POST https://your-server.com/github-webhook
```

Body có thông tin repository, commit, branch và người push.

=> Đây là Webhook pattern vì GitHub chủ động thông báo cho hệ thống bên ngoài khi có event.

### Kết luận về GitHub

GitHub API dùng CRUD để quản lý tài nguyên như issue và pull request, Query để lọc/tìm kiếm dữ liệu, HATEOAS-like để trả link liên quan, Event-driven để mô tả hoạt động trong repository, và Webhook để tích hợp CI/CD hoặc hệ thống tự động hóa.

---

## 3. So sánh nhanh Stripe và GitHub

| Pattern | Stripe | GitHub |
|---|---|---|
| CRUD | Customer, product, payment intent | Issue, pull request, repository, comment |
| Query | Lọc payment, charge, customer | Lọc issue, PR, search repository |
| HATEOAS | Ít nổi bật hơn | Rõ hơn qua các trường `url`, `comments_url`, `events_url` |
| Event-driven | Payment succeeded, invoice paid | Push, pull_request, issues |
| Webhook | Báo trạng thái thanh toán | Báo push code, PR, issue, workflow |

## Kết luận chung

Stripe và GitHub đều kết hợp nhiều API design patterns. CRUD và Query giúp client thao tác/lọc tài nguyên. Event-driven và Webhook giúp hệ thống phản ứng tự động khi có sự kiện. GitHub thể hiện HATEOAS rõ hơn Stripe vì response thường chứa nhiều link liên quan đến tài nguyên khác.
