from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI(title="Good Extensibility API")

db_table_users = {
    1: {
        "id_col": 1, 
        "full_name_col": "John Doe", 
        "is_active_flag": 1, 
        "legacy_password_hash": "xyz123"    
    }
}

class UserResponse(BaseModel):
    id: int
    name: str
    status: str
    links: List[Dict[str, str]]

def map_db_to_dto(db_user: dict, request: Request) -> UserResponse:
    user_id = db_user["id_col"]
    status_str = "ACTIVE" if db_user["is_active_flag"] == 1 else "INACTIVE"
    
    base_url = str(request.base_url).rstrip("/")
    
    links = [
        {"rel": "self", "href": f"{base_url}/api/v1/users/{user_id}"},
        {"rel": "update", "href": f"{base_url}/api/v1/users/{user_id}"},
        {"rel": "orders", "href": f"{base_url}/api/v1/users/{user_id}/orders"}
    ]
    
    if status_str == "INACTIVE":
        links.append({"rel": "activate", "href": f"{base_url}/api/v1/users/{user_id}/activate"})
        
    return UserResponse(
        id=user_id,
        name=db_user["full_name_col"],
        status=status_str,
        links=links
    )

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
def get_user_good(user_id: int, request: Request):
    if user_id not in db_table_users:
        raise HTTPException(status_code=404)
        
    db_user = db_table_users[user_id]
    
    return map_db_to_dto(db_user, request)
