from fastapi import FastAPI, HTTPException

app = FastAPI(title="Bad API Consistency")

users_data = {
    1: {"name": "Alice", "email": "alice@gmail.com"},
    2: {"name": "Bob", "email": "bob@gmail.com"}
}

@app.get("/api/v1/users/{user_id}")
def get_user_bad1(user_id: int):
    if user_id not in users_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return users_data[user_id] 

@app.get("/api/v1/users")
def get_users_bad2():
    return {"data": list(users_data.values())}

@app.delete("/api/v1/users/{user_id}")
def delete_user_bad3(user_id: int):
    if user_id not in users_data:
        return {"status": "error", "message": "Cannot delete, missing user!"}
        
    del users_data[user_id]
    return {"status": "success", "msg": "User deleted"}
