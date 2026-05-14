# Week 10 - Book Management Production API

API quan ly sach bang FastAPI, co cac thanh phan production co ban:

- CRUD sach
- API key cho thao tac ghi/sua/xoa
- Request logging va audit logs
- Prometheus metrics tai `/metrics`
- Rate limiting bang SlowAPI
- Circuit breaker mo phong service goi y sach ben ngoai
- Cau hinh qua `.env`

## Cai dat

```powershell
cd week10
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Chay API

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Mo Swagger UI:

```text
http://localhost:8000/docs
```

## Demo nhanh

### 1. Kiem tra API song

```powershell
Invoke-RestMethod http://localhost:8000/health
```

### 2. Tao sach moi

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/books `
  -Headers @{ "X-API-Key" = "demo-secret-key" } `
  -ContentType "application/json" `
  -Body '{"title":"Clean Architecture","author":"Robert C. Martin","year":2017,"category":"Software","available":true}'
```

### 3. Lay danh sach sach

```powershell
Invoke-RestMethod http://localhost:8000/books
```

### 4. Xem metrics Prometheus

```powershell
Invoke-WebRequest http://localhost:8000/metrics | Select-Object -ExpandProperty Content
```

### 5. Demo rate limit

Chay lenh tao sach nhieu hon 5 lan trong 1 phut. API se tra ve loi `429 Too Many Requests`.

### 6. Demo circuit breaker

```powershell
Invoke-RestMethod http://localhost:8000/external/recommendation
```

Goi nhieu lan. Endpoint nay mo phong service ben ngoai thinh thoang loi. Khi loi lien tiep, circuit breaker se mo va tra ve `503`.

## Noi dung can trinh bay

- `/health`: health check cho production.
- Console log: request log va audit log khi tao/sua/xoa sach.
- `/metrics`: Prometheus co the scrape metrics.
- Rate limit: bao ve endpoint ghi du lieu.
- API key: bao ve cac thao tac thay doi du lieu.
- Circuit breaker: ngan API phu thuoc qua lau vao service ngoai dang loi.

## Giai thich co che hien tai

### 1. Rate limit

Rate limit la co che gioi han so request ma mot client duoc gui trong mot khoang thoi gian. Trong bai nay, rate limit dung de bao ve endpoint ghi du lieu, tranh viec mot nguoi gui qua nhieu request tao sach lien tuc.

Thu vien dang dung:

- `slowapi`: thu vien rate limiting cho FastAPI/Starlette.
- `limits`: thu vien phu tro duoc `slowapi` su dung ben trong.

Cac file lien quan:

- `app/core/rate_limit.py`
- `app/core/config.py`
- `app/main.py`
- `app/routes/books.py`

Cach hoat dong:

1. Trong `app/core/config.py`, he thong khai bao cau hinh:

```python
rate_limit_default: str = "20/minute"
rate_limit_book_create: str = "5/minute"
```

Y nghia:

- Mac dinh moi client duoc gui toi da `20 request/phut`.
- Rieng endpoint tao sach chi duoc gui `5 request/phut`.

2. Trong `app/core/rate_limit.py`, tao doi tuong `Limiter`:

```python
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit_default])
```

`get_remote_address` lay dia chi IP cua client. Nhu vay moi IP se co mot bo dem request rieng.

3. Trong `app/main.py`, gan limiter vao FastAPI app va them middleware:

```python
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
```

Y nghia:

- `SlowAPIMiddleware` kiem tra moi request di vao.
- Neu client gui qua so luong cho phep, FastAPI tra ve loi `429 Too Many Requests`.
- `_rate_limit_exceeded_handler` tao response loi chuan cho truong hop vuot gioi han.

4. Trong `app/routes/books.py`, endpoint tao sach co decorator:

```python
@limiter.limit(settings.rate_limit_book_create)
def create_book(...):
```

Y nghia: endpoint `POST /books` bi gioi han rieng la `5 request/phut`. Neu goi lan thu 6 trong cung mot phut, API se tra ve `429`.

Cach demo:

- Mo Swagger tai `http://localhost:8000/docs`.
- Goi `POST /books` lien tuc hon 5 lan trong 1 phut.
- Ket qua mong doi: nhung lan dau thanh cong `201`, sau do bi chan voi `429 Too Many Requests`.

Noi ngan gon khi thuyet trinh:

> Em dung SlowAPI de gioi han tan suat request theo IP. Endpoint tao sach duoc gioi han 5 lan/phut. Khi client gui qua nhieu request, middleware se chan va tra ve 429, giup bao ve API khoi spam hoac lam dung.

### 2. Circuit breaker

Circuit breaker la co che bao ve API khi mot service ben ngoai bi loi lien tuc. Thay vi tiep tuc goi service dang loi va lam cham/he thong bi treo, circuit breaker se tam thoi "ngat mach" va tra loi nhanh rang service dang khong san sang.

Thu vien dang dung:

- `pybreaker`: cai dat mau circuit breaker trong Python.

Cac file lien quan:

- `app/core/circuit_breaker.py`
- `app/routes/external.py`

Cach hoat dong:

1. Trong `app/core/circuit_breaker.py`, tao circuit breaker:

```python
recommendation_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=20)
```

Y nghia:

- `fail_max=3`: neu service loi 3 lan lien tiep, circuit breaker chuyen sang trang thai open.
- `reset_timeout=20`: sau 20 giay, circuit breaker cho thu lai mot request.

2. Ham mo phong goi service ngoai:

```python
@recommendation_breaker
def fetch_recommendation_from_external_service() -> dict[str, str]:
```

Decorator `@recommendation_breaker` bao quanh ham goi service. Neu ham nem loi nhieu lan lien tiep, breaker se tu dong mo.

Trong bai nay service ngoai duoc mo phong bang random:

```python
if random.random() < 0.45:
    raise ConnectionError("Recommendation service is temporarily unavailable")
```

Y nghia: khoang 45% request se bi gia lap loi de co the demo circuit breaker.

3. Trong `app/routes/external.py`, endpoint `/external/recommendation` goi ham tren:

```python
result = fetch_recommendation_from_external_service()
```

Neu service thanh cong, API tra ve goi y sach. Neu service loi, API tra ve `503 Service Unavailable`. Neu breaker da open, API cung tra ve `503` nhung thong bao la circuit breaker dang chan tam thoi.

Trang thai circuit breaker co 3 trang thai chinh:

- `closed`: binh thuong, request van duoc goi den service ngoai.
- `open`: service loi qua nhieu lan, breaker chan request ngay lap tuc.
- `half-open`: sau thoi gian cho, breaker thu cho mot request di qua de xem service da hoi phuc chua.

Cach demo:

```powershell
Invoke-RestMethod http://localhost:8000/external/recommendation
```

Goi lenh nay nhieu lan. Do service duoc mo phong loi ngau nhien, ban se thay co luc thanh cong, co luc tra `503`. Neu gap nhieu loi lien tiep, circuit breaker se mo va tiep tuc tra `503` nhanh ma khong can goi service mo phong nua.

Noi ngan gon khi thuyet trinh:

> Em dung PyBreaker de cai dat circuit breaker cho endpoint goi y sach. Service goi y duoc gia lap la service ben ngoai va co kha nang loi. Neu loi 3 lan lien tiep, circuit breaker se mo trong 20 giay va API tra ve 503 ngay, tranh viec he thong tiep tuc phu thuoc vao service dang loi.

### 3. Lien he voi production

Trong moi truong production, rate limit va circuit breaker la hai co che bao ve API:

- Rate limit bao ve API khoi spam, brute force, hoac client gui request qua muc.
- Circuit breaker bao ve API khi service phu thuoc ben ngoai bi cham hoac bi loi.

Trong bai nay chi dung cau hinh don gian de demo, nhung y tuong giong voi he thong production that: API can co co che tu bao ve va giam sat thay vi chi co CRUD co ban.
