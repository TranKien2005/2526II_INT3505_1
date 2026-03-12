from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Bad Extensibility API")

db_table_users = {
    1: {
        "id_col": 1, 
        "full_name_col": "John Doe",    
        "is_active_flag": 1, 
        "legacy_password_hash": "xyz123"
    }
}

@app.get("/api/v1/users/{user_id}")
def get_user_bad(user_id: int):
    if user_id not in db_table_users:
        raise HTTPException(status_code=404)
        
    return db_table_users[user_id]
