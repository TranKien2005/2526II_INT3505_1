from fastapi import FastAPI, HTTPException, status, UploadFile, File, Depends, Query, Path
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Thực hành REST API với FastAPI")

users_db = {
    123: {"id": 123, "name": "Nguyen Van A", "email": "a@example.com", "role": "user"}
}
comments_db = {
    456: {"id": 456, "content": "Bình luận vi phạm", "author_id": 999}
}

class EmailUpdate(BaseModel):
    email: EmailStr

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

def verify_token(token: str = "valid_token"):
    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )
    return True

@app.get("/api/v1/users", tags=["Users"])
def get_users(
    page: int = Query(1, ge=1, description="Trang hiện tại"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng trên 1 trang")
):
    return {
        "page": page,
        "limit": limit,
        "total": len(users_db),
        "users": list(users_db.values())
    }

@app.patch("/api/v1/users/{user_id}/email", tags=["Users"])
def update_user_email(
    user_id: int, 
    payload: EmailUpdate, 
    is_authenticated: bool = Depends(verify_token)
):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng (404 Not Found)"
        )
    
    for u in users_db.values():
        if u["email"] == payload.email and u["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email này đã được sử dụng (409 Conflict)"
            )
            
    users_db[user_id]["email"] = payload.email
    return {"message": "Cập nhật email thành công", "user": users_db[user_id]}

@app.post("/api/v1/posts", status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(post: PostCreate, is_authenticated: bool = Depends(verify_token)):
    if post.title == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi máy chủ nội bộ khi lưu bài viết (500 Internal Server Error)"
        )
        
    return {"message": "Tạo bài viết thành công", "post_id": 789, "data": post}

@app.delete("/api/v1/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comments"])
def delete_comment(
    comment_id: int, 
    user_role: str = "user",
    is_authenticated: bool = Depends(verify_token)
):
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa bình luận này (403 Forbidden)"
        )
        
    if comment_id not in comments_db:
        raise HTTPException(status_code=404, detail="Không tìm thấy bình luận")
        
    del comments_db[comment_id]
    return

@app.post("/api/v1/users/{user_id}/avatar", tags=["Users"])
def upload_avatar(
    user_id: int, 
    avatar: UploadFile = File(...),
    is_authenticated: bool = Depends(verify_token)
):
    if not avatar.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Định dạng file không hỗ trợ, vui lòng tải lên hình ảnh (400 Bad Request)"
        )

    file_size_bytes = len(avatar.file.read())
    
    if file_size_bytes > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Kích thước file vượt quá 5MB. (413 Payload Too Large)"
        )
        
    return {
        "message": "Upload thành công",
        "filename": avatar.filename,
        "content_type": avatar.content_type
    }
