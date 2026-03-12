from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Bad Versioning API")

class UserUpdate(BaseModel):
    first_name: str
    last_name: str

users_db = {
    1: {"first_name": "John", "last_name": "Doe"}
}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return users_db.get(user_id)

@app.put("/api/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate):
    users_db[user_id] = {"first_name": payload.first_name, "last_name": payload.last_name}
    return users_db[user_id]
