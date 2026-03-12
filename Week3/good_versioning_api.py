from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Good Versioning API")

users_db = {
    1: {"name": "John Doe", "first_name": "John", "last_name": "Doe"}
}

class UserUpdateV1(BaseModel):
    name: str

@app.get("/api/v1/users/{user_id}", tags=["Version 1 (Legacy)"])
def get_user_v1(user_id: int):
    user = users_db.get(user_id)
    if user:
        return {"name": user["name"]}
    return None

@app.put("/api/v1/users/{user_id}", tags=["Version 1 (Legacy)"])
def update_user_v1(user_id: int, payload: UserUpdateV1):
    parts = payload.name.split(" ", 1)
    f_name = parts[0]
    l_name = parts[1] if len(parts) > 1 else ""
    
    users_db[user_id] = {
        "name": payload.name,
        "first_name": f_name,
        "last_name": l_name
    }
    return {"name": users_db[user_id]["name"]}

class UserUpdateV2(BaseModel):
    first_name: str
    last_name: str

@app.get("/api/v2/users/{user_id}", tags=["Version 2 (Current)"])
def get_user_v2(user_id: int):
    user = users_db.get(user_id)
    if user:
        return {"first_name": user["first_name"], "last_name": user["last_name"]}
    return None

@app.put("/api/v2/users/{user_id}", tags=["Version 2 (Current)"])
def update_user_v2(user_id: int, payload: UserUpdateV2):
    full_name = f"{payload.first_name} {payload.last_name}".strip()
    
    users_db[user_id] = {
        "name": full_name,
        "first_name": payload.first_name,
        "last_name": payload.last_name
    }
    return {
        "first_name": users_db[user_id]["first_name"],
        "last_name": users_db[user_id]["last_name"]
    }
