from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import date

app = FastAPI(
    title="Library Management API",
    description="API quản lý thư viện bao gồm Sách, Người dùng và Phiếu mượn.",
    version="1.1.0"
)

# --- Pydantic Models ---

class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(..., example="Nguyễn Văn A")

class BookInput(BaseModel):
    title: str = Field(..., example="Lão Hạc")
    author: Optional[str] = Field(None, example="Nam Cao")
    publishedYear: Optional[int] = Field(None, example=1943)
    isbn: Optional[str] = Field(None, example="978-604-1-23456-7")

class Book(BookInput):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

class BorrowTicket(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    book_id: uuid.UUID
    borrow_date: date = Field(default_factory=date.today)

class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int

class PaginatedBooksResponse(BaseModel):
    data: List[Book]
    meta: PaginationMeta

class ErrorResponse(BaseModel):
    errorCode: str
    message: str

# --- In-Memory Databases ---

users_db: List[User] = []
books_db: List[Book] = [
    Book(id=uuid.uuid4(), title="Lão Hạc", author="Nam Cao", publishedYear=1943),
    Book(id=uuid.uuid4(), title="Số Đỏ", author="Vũ Trọng Phụng", publishedYear=1936),
    Book(id=uuid.uuid4(), title="Tắt Đèn", author="Ngô Tất Tố", publishedYear=1937),
    Book(id=uuid.uuid4(), title="Chiếc Lược Ngà", author="Nguyễn Quang Sáng", publishedYear=1966),
    Book(id=uuid.uuid4(), title="Dế Mèn Phiêu Lưu Ký", author="Tô Hoài", publishedYear=1941)
]
tickets_db: List[BorrowTicket] = []

# --- Book Endpoints ---

@app.get("/books", response_model=PaginatedBooksResponse, summary="Tìm kiếm và phân trang sách")
def search_and_paginate_books(
    q: Optional[str] = Query(None, description="Từ khóa tìm kiếm theo tiêu đề hoặc tác giả"),
    page: int = Query(1, ge=1, description="Số trang hiện tại"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng bản ghi mỗi trang")
):
    """
    Tìm kiếm sách theo tiêu đề hoặc tác giả và trả về kết quả đã được phân trang.
    """
    filtered_books = books_db
    if q:
        q_lower = q.lower()
        filtered_books = [
            b for b in books_db 
            if q_lower in b.title.lower() or (b.author and q_lower in b.author.lower())
        ]
    
    total = len(filtered_books)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = filtered_books[start:end]

    return PaginatedBooksResponse(
        data=paginated_data,
        meta=PaginationMeta(total=total, page=page, limit=limit)
    )

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Thêm một cuốn sách mới")
def create_book(book_in: BookInput):
    new_book = Book(**book_in.dict())
    books_db.append(new_book)
    return new_book

@app.get("/books/{book_id}", response_model=Book, summary="Lấy thông tin chi tiết một cuốn sách")
def get_book(book_id: uuid.UUID):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Không tìm thấy sách.")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa một cuốn sách")
def delete_book(book_id: uuid.UUID):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Không tìm thấy sách.")

# --- User Endpoints ---

@app.get("/users", response_model=List[User], summary="Lấy danh sách người dùng")
def get_users():
    return users_db

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, summary="Tạo người dùng mới")
def create_user(name: str = Query(..., example="Nguyễn Văn A")):
    new_user = User(name=name)
    users_db.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=User, summary="Lấy thông tin người dùng")
def get_user(user_id: uuid.UUID):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

# --- BorrowTicket Endpoints ---

@app.get("/borrow-tickets", response_model=List[BorrowTicket], summary="Lấy danh sách phiếu mượn")
def get_tickets():
    return tickets_db

@app.post("/borrow-tickets", response_model=BorrowTicket, status_code=status.HTTP_201_CREATED, summary="Tạo phiếu mượn sách mới")
def create_ticket(user_id: uuid.UUID, book_id: uuid.UUID, borrow_date: Optional[date] = None):
    # Verify user exists
    if not any(u.id == user_id for u in users_db):
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại.")
    
    # Verify book exists
    if not any(b.id == book_id for b in books_db):
        raise HTTPException(status_code=404, detail="Sách không tồn tại.")
        
    new_ticket = BorrowTicket(
        user_id=user_id,
        book_id=book_id,
        borrow_date=borrow_date or date.today()
    )
    tickets_db.append(new_ticket)
    return new_ticket

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
