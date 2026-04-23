# Script khei động MongoDB phục vụ lập trình Local
Write-Host "dang khoi dong MongoDB trong Docker..." -ForegroundColor Cyan

# Chỉ bật service mongodb, không build/bật service python
docker compose up -d mongodb

Write-Host "`n==========================================" -ForegroundColor Green
Write-Host "MongoDB dã san sàng tai: localhost:27017" -ForegroundColor Green
Write-Host "Ban co the chay Server bang lenh:" -ForegroundColor Yellow
Write-Host "uvicorn openapi_server.main:app --reload" -ForegroundColor Yellow
Write-Host "==========================================`n" -ForegroundColor Green
