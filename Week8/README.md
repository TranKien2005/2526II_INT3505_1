# Week8 - Library Management API (FastAPI + MySQL)

## 1) Khởi động nhanh

### Bước 1: Cài dependency (dùng `.venv` chung ở root)
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy MySQL bằng Docker (chỉ DB)
```bash
docker compose -f Week8/docker-compose.yml up -d
```

### Bước 3: Chạy API trên máy thật
```bash
MYSQL_HOST=127.0.0.1 MYSQL_PORT=3306 MYSQL_USER=library_user MYSQL_PASSWORD=library_password MYSQL_DB=library_db python -m uvicorn Week8.app.main:app --host 0.0.0.0 --port 8000
```

Mở Swagger:
- http://127.0.0.1:8000/docs

## 2) Chạy test nhanh

### Unit test
```bash
python -m pytest Week8/tests/unit -q
```

### Integration test
```bash
python -m pytest Week8/tests/integration -q
```

### Chạy toàn bộ test Python
```bash
python -m pytest Week8/tests -q
```

## 3) Performance test (k6)

### Cài k6 local vào Week8/tools/k6 (nếu chưa có)
```bash
mkdir -p Week8/tools/k6
curl -L https://github.com/grafana/k6/releases/download/v0.51.0/k6-v0.51.0-windows-amd64.zip -o Week8/tools/k6/k6.zip
python -c "import zipfile; zipfile.ZipFile('Week8/tools/k6/k6.zip').extractall('Week8/tools/k6')"
```

### Chạy k6 (Windows PowerShell)
```powershell
& 'D:\My Works\Coding\Practice\2526II_INT3505_1\Week8\tools\k6\k6-v0.51.0-windows-amd64\k6.exe' run -e BASE_URL=http://127.0.0.1:8000 'D:\My Works\Coding\Practice\2526II_INT3505_1\Week8\tests\performance\k6_library.js'
```

## 4) API integration test bằng Newman (Postman CLI)

### Cài Newman local ở root project (1 lần)
```bash
npm install --save-dev newman
```

### Chạy collection Week8 bằng npx
```bash
npx newman run Week8/Week8-Library.postman_collection.json
```

## 5) Dọn môi trường

### Dừng MySQL container
```bash
docker compose -f Week8/docker-compose.yml down
```

### Dừng và xóa luôn dữ liệu DB
```bash
docker compose -f Week8/docker-compose.yml down -v
```
