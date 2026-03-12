from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Bad API Naming (Không chuẩn REST)")

class UserInput(BaseModel):
    name: str

class AddressInput(BaseModel):
    city: str

@app.post("/api/v1/createUser")
def create_user(payload: UserInput):
    return {"message": "Tạo user thành công"}

@app.get("/api/v1/get_all_users")
def get_all_users():
    return {"message": "Lấy danh sách user"}

@app.get("/api/v1/user/{UserId}/GetAddress")
def get_user_address(UserId: int):
    return {"message": f"Trả về địa chỉ của user có ID {UserId}"}

@app.put("/api/v1/UpdateUserProfile/{id}")
def update_profile(id: int):
    return {"message": "Sửa profile thành công"}
