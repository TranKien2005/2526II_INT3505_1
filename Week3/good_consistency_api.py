from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Optional

app = FastAPI(title="Good API Consistency (Phản hồi Chuẩn hóa)")

users_data = {
    1: {"name": "Alice", "email": "alice@gmail.com"},
    2: {"name": "Bob", "email": "bob@gmail.com"}
}

def standard_response(
    success: bool,
    data: Optional[Any] = None,
    error: Optional[str] = None,
    meta: Optional[dict] = None
) -> dict:
    return {
        "success": success,
        "data": data,
        "error": error,
        "meta": meta
    }

@app.get("/api/v1/users/{user_id}", tags=["Users"])
def get_user_good1(user_id: int):
    if user_id not in users_data:
        raise HTTPException(status_code=404, detail="User not found")
        
    return standard_response(
        success=True, 
        data=users_data[user_id]
    )

@app.get("/api/v1/users", tags=["Users"])
def get_users_good2(page: int = 1, limit: int = 10):
    users_list = list(users_data.values())
    
    return standard_response(
        success=True, 
        data=users_list,
        meta={
            "page": page,
            "limit": limit,
            "total": len(users_list)
        }
    )

@app.delete("/api/v1/users/{user_id}", tags=["Users"])
def delete_user_good3(user_id: int):
    if user_id not in users_data:
        raise HTTPException(status_code=404, detail="User not found")
        
    del users_data[user_id]
    
    return standard_response(
        success=True,
        data=None,
        meta={"message": "User deleted successfully"}
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Bắt mọi lỗi HTTPException và ép nó tuân theo khung standard_response
    thay vì cái khung lỗi mặc định cứng nhắc của FastAPI
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=standard_response(
            success=False,
            data=None,
            error=str(exc.detail)
        )
    )
