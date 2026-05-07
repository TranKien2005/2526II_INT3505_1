from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import uuid

app = FastAPI(title="Payment API v1", version="1.0.0")

# Mock database
payments_db = {}

class PaymentRequest(BaseModel):
    amount: float
    currency: str
    card_number: str
    description: str = "Payment v1"

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str

@app.post("/v1/payments", response_model=PaymentResponse)
async def create_payment(request: PaymentRequest):
    # Simulate payment processing
    payment_id = str(uuid.uuid4())
    payment_data = {
        "payment_id": payment_id,
        "status": "completed",
        "amount": request.amount,
        "currency": request.currency,
        "card_number": request.card_number, # Security issue in v1: storing raw card number
        "description": request.description
    }
    payments_db[payment_id] = payment_data
    return payment_data

@app.get("/v1/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str):
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments_db[payment_id]

if __name__ == "__main__":
    print("Starting Payment API v1 on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
