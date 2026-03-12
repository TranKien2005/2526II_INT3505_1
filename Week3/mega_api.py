from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="Mega All-in-One API (Bad Practice cho hệ thống lớn)")

db = {
    "users": {
        1: {"id": 1, "name": "Nguyễn Văn A", "email": "a@example.com"}
    },
    "orders": {
        101: {"id": 101, "user_id": 1, "product": "Laptop", "price": 1500, "status": "pending"}
    },
    "shipping": {
        201: {"id": 201, "order_id": 101, "address": "Hà Nội", "shipped": False}
    }
}

class MegaRequest(BaseModel):
    action: str
    user_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    product: Optional[str] = None
    price: Optional[float] = None
    shipping_address: Optional[str] = None

@app.post("/api/v1/do_everything")
def do_everything(payload: MegaRequest):
    
    if payload.action == "add_user":
        if not payload.user_id or not payload.name or not payload.email:
            raise HTTPException(status_code=400, detail="Thiếu thông tin tạo User!")
            
        if payload.user_id in db["users"]:
            raise HTTPException(status_code=409, detail="User ID đã tồn tại")
            
        db["users"][payload.user_id] = {
            "id": payload.user_id,
            "name": payload.name,
            "email": payload.email
        }
        return {"message": "Thêm User thành công", "data": db["users"][payload.user_id]}
        
    elif payload.action == "update_user":
        if not payload.user_id or not payload.email:
            raise HTTPException(status_code=400, detail="Thiếu User ID hoặc Email mới!")
            
        if payload.user_id not in db["users"]:
            raise HTTPException(status_code=404, detail="Không tìm thấy User!")
            
        db["users"][payload.user_id]["email"] = payload.email
        return {"message": "Sửa Email thành công", "data": db["users"][payload.user_id]}

    elif payload.action == "checkout":
        if not payload.user_id or not payload.product or not payload.price or not payload.shipping_address:
            raise HTTPException(status_code=400, detail="Thiếu thông tin thanh toán!")
            
        if payload.user_id not in db["users"]:
            raise HTTPException(status_code=404, detail="Chỉ User đã đăng ký mới được Checkout!")

        new_order_id = len(db["orders"]) + 101
        db["orders"][new_order_id] = {
            "id": new_order_id,
            "user_id": payload.user_id,
            "product": payload.product,
            "price": payload.price,
            "status": "pending"
        }

        new_shipping_id = len(db["shipping"]) + 201
        db["shipping"][new_shipping_id] = {
            "id": new_shipping_id,
            "order_id": new_order_id,
            "address": payload.shipping_address,
            "shipped": False
        }

        return {
            "message": "Checkout thành công", 
            "order_id": new_order_id,
            "shipping_id": new_shipping_id
        }
        
    else:
        raise HTTPException(status_code=400, detail=f"Hành động '{payload.action}' không được hỗ trợ!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
