from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta, timezone
import uuid
import jwt
import bcrypt
import json
import os

# ======================== CONFIG ========================
SECRET_KEY = "my-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="Book Management API (JWT)",
    description="""
API quản lý sách có xác thực JWT. 

### Hướng dẫn sử dụng:
1. **Lấy Token**: Sử dụng endpoint `/auth/login` (với user **admin** / **password123**) để lấy `access_token`.
2. **Xác thực**: Nhấn nút **Authorize** màu xanh phía trên.
3. **Dán Token**: Dán trực tiếp Token bạn vừa lấy vào ô **Value** (không cần gõ thêm chữ 'Bearer').
4. **Thử nghiệm**: Sau khi nhấn Authorize, các lệnh trong nhóm **Books** sẽ hoạt động.

*Ghi chú: Dữ liệu (User và Book) được lưu bền vững vào file `data_week6.json`.*
""",
    version="2.1.0",
)

# ======================== SECURITY ========================
security = HTTPBearer()
# Note: Keeping the tokenUrl for existing login logic if needed, 
# but using HTTPBearer for the "Authorize" button in Swagger.
oauth2_scheme = security 


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    """Giải mã JWT token và trả về user hiện tại."""
    token = auth.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = next((u for u in users_db if u["username"] == username), None)
    if user is None:
        raise credentials_exception
    return user


# ======================== MODELS ========================
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, example="admin")
    password: str = Field(..., min_length=6, example="secret123")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BookInput(BaseModel):
    title: str = Field(..., example="Số Đỏ")
    author: str = Field(..., example="Vũ Trọng Phụng")
    publishedYear: Optional[int] = Field(None, example=1936)
    isbn: Optional[str] = Field(None, example="978-604-1-08108-4")


class Book(BookInput):
    id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")


class ErrorResponse(BaseModel):
    errorCode: str
    message: str


# ======================== PERSISTENCE ========================
DATA_FILE = os.path.join(os.path.dirname(__file__), "data_week6.json")
users_db: list[dict] = []      # [{username, hashed_password}]
fake_database: List[Book] = []

def load_data():
    global users_db, fake_database
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_db = data.get("users", [])
                # Re-construct Pydantic objects for books
                fake_database = [Book(**b) for b in data.get("books", [])]
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Seed default admin if no users exist
    if not users_db:
        users_db.append({
            "username": "admin",
            "hashed_password": hash_password("password123"),
        })
        save_data()

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "users": users_db,
                "books": [b.model_dump() for b in fake_database]
            }, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data: {e}")

# Initial load
load_data()


# ======================== AUTH ENDPOINTS ========================
@app.post(
    "/auth/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
    tags=["Auth"],
)
def register(user_in: UserRegister):
    """Tạo tài khoản người dùng mới. Mật khẩu được hash bằng bcrypt."""
    if any(u["username"] == user_in.username for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại.",
        )
    users_db.append({
        "username": user_in.username,
        "hashed_password": hash_password(user_in.password),
    })
    save_data()
    return {"message": f"Đăng ký thành công cho user '{user_in.username}'."}


@app.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Đăng nhập và nhận JWT token",
    tags=["Auth"],
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Xác thực username/password, trả về JWT access token."""
    user = next((u for u in users_db if u["username"] == form_data.username), None)
    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user["username"]})
    return TokenResponse(access_token=token)


# ======================== PROTECTED ME ENDPOINT ========================
@app.get(
    "/auth/me",
    summary="Kiểm tra thông tin user hiện tại",
    tags=["Auth"],
)
def get_me(current_user: dict = Depends(get_current_user)):
    """Trả về thông tin của user gắn với token hiện tại."""
    return {"username": current_user["username"], "status": "authorized"}


# ======================== BOOK ENDPOINTS (PROTECTED) ========================
@app.get(
    "/books",
    response_model=List[Book],
    summary="Lấy danh sách tất cả các cuốn sách",
    tags=["Books"],
)
def get_all_books(current_user: dict = Depends(get_current_user)):
    """Trả về danh sách sách hiện có trong hệ thống. Yêu cầu JWT token."""
    return fake_database


@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm một cuốn sách mới",
    tags=["Books"],
)
def create_new_book(book_in: BookInput, current_user: dict = Depends(get_current_user)):
    """Tạo mới một bản ghi sách trong hệ thống."""
    new_book = Book(
        id=str(uuid.uuid4()),
        title=book_in.title,
        author=book_in.author,
        publishedYear=book_in.publishedYear,
        isbn=book_in.isbn,
    )
    fake_database.append(new_book)
    save_data()
    return new_book


@app.get(
    "/books/{bookId}",
    response_model=Book,
    summary="Lấy thông tin chi tiết một cuốn sách",
    tags=["Books"],
)
def get_book_by_id(bookId: str, current_user: dict = Depends(get_current_user)):
    """Lấy thông tin chi tiết của một cuốn sách dựa trên ID cung cấp."""
    for b in fake_database:
        if b.id == bookId:
            return b
    raise HTTPException(status_code=404, detail="Không tìm thấy sách với ID này.")


@app.put(
    "/books/{bookId}",
    response_model=Book,
    summary="Cập nhật thông tin sách",
    tags=["Books"],
)
def update_book(bookId: str, book_in: BookInput, current_user: dict = Depends(get_current_user)):
    """Cập nhật toàn bộ nội dung thông tin của một cuốn sách."""
    for i, b in enumerate(fake_database):
        if b.id == bookId:
            updated_book = Book(
                id=bookId,
                title=book_in.title,
                author=book_in.author,
                publishedYear=book_in.publishedYear,
                isbn=book_in.isbn,
            )
            fake_database[i] = updated_book
            save_data()
            return updated_book
    raise HTTPException(status_code=404, detail="Không tìm thấy sách để cập nhật.")


@app.delete(
    "/books/{bookId}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa một cuốn sách",
    tags=["Books"],
)
def delete_book(bookId: str, current_user: dict = Depends(get_current_user)):
    """Xóa cuốn sách khỏi hệ thống dựa trên ID."""
    for i, b in enumerate(fake_database):
        if b.id == bookId:
            fake_database.pop(i)
            save_data()
            return None
    raise HTTPException(status_code=404, detail="Không tìm thấy sách để xóa.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
