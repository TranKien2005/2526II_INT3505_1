from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import uvicorn
import uuid
from typing import Optional, Dict

app = FastAPI(
    title="Payment API v2", 
    version="2.0.0",
    description="Phiên bản nâng cấp với bảo mật Tokenization và cấu trúc dữ liệu mới."
)

# Mock database (shared for both versions in this example)
payments_db = {}

# --- SCHEMAS FOR V1 (Legacy) ---
class PaymentRequestV1(BaseModel):
    amount: float
    currency: str
    card_number: str

class PaymentResponseV1(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str

# --- SCHEMAS FOR V2 (Modern) ---
class PaymentRequestV2(BaseModel):
    amount: float = Field(..., gt=0, description="Số tiền thanh toán")
    currency: str = Field(..., min_length=3, max_length=3, description="Mã tiền tệ ISO (VD: USD, VND)")
    payment_method_id: str = Field(..., description="Token đại diện cho phương thức thanh toán (PCI-DSS compliant)")
    metadata: Optional[Dict[str, str]] = None

class PaymentResponseV2(BaseModel):
    id: str
    status: str
    amount: float
    currency: str
    payment_method_details: Dict[str, str]
    created_at: str
    metadata: Dict[str, str]

# --- V1 ROUTES (Deprecated) ---
@app.post("/v1/payments", response_model=PaymentResponseV1, tags=["Legacy V1"])
async def create_payment_v1(request: PaymentRequestV1, response: Response):
    # Thêm header cảnh báo Deprecation
    response.headers["Warning"] = '299 - "v1 is deprecated. Please migrate to /v2/payments by 2026-11-07."'
    
    payment_id = f"v1_{uuid.uuid4()}"
    payment_data = {
        "payment_id": payment_id,
        "status": "completed",
        "amount": request.amount,
        "currency": request.currency,
        "card_number": request.card_number,
    }
    payments_db[payment_id] = payment_data
    return payment_data

@app.get("/v1/payments/{payment_id}", response_model=PaymentResponseV1, tags=["Legacy V1"])
async def get_payment_v1(payment_id: str, response: Response):
    response.headers["Warning"] = '299 - "v1 is deprecated."'
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments_db[payment_id]

# --- V2 ROUTES (Current) ---
@app.post("/v2/payments", response_model=PaymentResponseV2, tags=["Modern V2"])
async def create_payment_v2(request: PaymentRequestV2):
    payment_id = f"v2_{uuid.uuid4()}"
    
    # Giả lập xử lý với Token thay vì Card Number
    payment_data = {
        "id": payment_id,
        "status": "succeeded",
        "amount": request.amount,
        "currency": request.currency.upper(),
        "payment_method_details": {
            "type": "card",
            "last4": "4242", # Lấy từ token (giả lập)
            "token_used": request.payment_method_id
        },
        "created_at": "2026-05-07T16:00:00Z",
        "metadata": request.metadata or {}
    }
    payments_db[payment_id] = payment_data
    return payment_data

@app.get("/v2/payments/{payment_id}", response_model=PaymentResponseV2, tags=["Modern V2"])
async def get_payment_v2(payment_id: str):
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    data = payments_db[payment_id]
    
    # Nếu là data từ v1, ta cần map lại sang format v2 (Adapter pattern)
    if payment_id.startswith("v1_"):
        return {
            "id": data["payment_id"],
            "status": "succeeded",
            "amount": data["amount"],
            "currency": data["currency"],
            "payment_method_details": {"type": "legacy_card", "last4": "****"},
            "created_at": "N/A",
            "metadata": {"source": "migrated_from_v1"}
        }
    
    return data

if __name__ == "__main__":
    print("Starting Payment API (v1 & v2) on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
