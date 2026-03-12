from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Bounded Context API")

user_db = {
    1: {"id": 1, "name": "Nguyễn Văn A", "email": "a@example.com"}
}

order_db = {
    101: {"id": 101, "user_id": 1, "product": "Laptop", "price": 1500, "status": "pending"}
}

shipping_db = {
    201: {"id": 201, "order_id": 101, "address": "Hà Nội", "shipped": False}
}

class UserCreateRequest(BaseModel):
    user_id: int
    name: str
    email: EmailStr

class UserUpdateRequest(BaseModel):
    email: EmailStr

class OrderCreateRequest(BaseModel):
    user_id: int
    product: str
    price: float

class ShippingCreateRequest(BaseModel):
    order_id: int
    address: str

class CheckoutRequest(BaseModel):
    user_id: int
    product: str
    price: float
    shipping_address: str

@app.post("/api/v1/users", tags=["User Context"])
def create_user(payload: UserCreateRequest):
    if payload.user_id in user_db:
        raise HTTPException(status_code=409, detail="User ID đã tồn tại")
        
    user_db[payload.user_id] = {
        "id": payload.user_id,
        "name": payload.name,
        "email": payload.email
    }
    return {"message": "Thêm User thành công", "data": user_db[payload.user_id]}

@app.put("/api/v1/users/{user_id}/email", tags=["User Context"])
def update_user_email(user_id: int, payload: UserUpdateRequest):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="Không tìm thấy User!")
        
    user_db[user_id]["email"] = payload.email
    return {"message": "Sửa Email thành công", "data": user_db[user_id]}

@app.post("/api/v1/orders", tags=["Order Context"])
def create_order(payload: OrderCreateRequest):
    if payload.user_id not in user_db:
        raise HTTPException(status_code=404, detail="User không tồn tại")
        
    if payload.price < 0:
        raise HTTPException(status_code=400, detail="Giá không hợp lệ")
        
    new_order_id = len(order_db) + 101
    order_db[new_order_id] = {
        "id": new_order_id,
        "user_id": payload.user_id,
        "product": payload.product,
        "price": payload.price,
        "status": "pending"
    }

    return {"message": "Tạo đơn hàng thành công", "order_id": new_order_id, "data": order_db[new_order_id]}

@app.post("/api/v1/shipping", tags=["Shipping Context"])
def create_shipping(payload: ShippingCreateRequest):
    if payload.address == "":
        raise HTTPException(status_code=400, detail="Thiếu địa chỉ giao hàng")
        
    new_shipping_id = len(shipping_db) + 201
    shipping_db[new_shipping_id] = {
        "id": new_shipping_id,
        "order_id": payload.order_id,
        "address": payload.address,
        "shipped": False
    }

    return {"message": "Tạo lệnh vận chuyển thành công", "shipping_id": new_shipping_id}

@app.post("/api/v1/checkout", tags=["Gateway API"])
def checkout_orchestrator(payload: CheckoutRequest):
    if payload.user_id not in user_db:
        raise HTTPException(status_code=404, detail="Vui lòng tạo User trước!")
        
    order_req = OrderCreateRequest(
        user_id=payload.user_id,
        product=payload.product,
        price=payload.price
    )
    order_res = create_order(order_req)
    
    shipping_req = ShippingCreateRequest(
        order_id=order_res["order_id"],
        address=payload.shipping_address
    )
    shipping_res = create_shipping(shipping_req)
    
    return {
        "message": "Checkout thành công",
        "order_id": order_res["order_id"],
        "shipping_id": shipping_res["shipping_id"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
