from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Good API Naming (Chuẩn REST)")

class UserInput(BaseModel):
    name: str

class AddressInput(BaseModel):
    city: str

@app.post("/api/v1/users", tags=["Users"])
def create_user(payload: UserInput):
    return {"message": "Tạo user thành công"}

@app.get("/api/v1/users", tags=["Users"])
def get_all_users():
    return {"message": "Lấy danh sách user"}

@app.get("/api/v1/users/{user_id}/address", tags=["Users"])
def get_user_address(user_id: int):
    return {"message": f"Trả về địa chỉ của user có ID {user_id}"}

@app.put("/api/v1/users/{user_id}/profile", tags=["Users"])
def update_profile(user_id: int):
    return {"message": f"Sửa profile của user {user_id} thành công"}
