from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

app = FastAPI(
    title="Book Management API",
    description="API quản lý sách (Book Management System) cung cấp các endpoint để thêm, sửa, xóa và truy vấn thông tin sách.",
    version="1.0.0"
)

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

fake_database: List[Book] = []

@app.get("/books", response_model=List[Book], summary="Lấy danh sách tất cả các cuốn sách")
def get_all_books():
    """Trả về danh sách sách hiện có trong hệ thống. Có thể hỗ trợ phân trang sau này."""
    return fake_database

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Thêm một cuốn sách mới")
def create_new_book(book_in: BookInput):
    """Tạo mới một bản ghi sách trong hệ thống."""
    new_book = Book(
        id=str(uuid.uuid4()),
        title=book_in.title,
        author=book_in.author,
        publishedYear=book_in.publishedYear,
        isbn=book_in.isbn
    )
    fake_database.append(new_book)
    return new_book

@app.get("/books/{bookId}", response_model=Book, summary="Lấy thông tin chi tiết một cuốn sách")
def get_book_by_id(bookId: str):
    """Lấy thông tin chi tiết của một cuốn sách dựa trên ID cung cấp."""
    for b in fake_database:
        if b.id == bookId:
            return b
    raise HTTPException(status_code=404, detail="Không tìm thấy sách với ID này.")

@app.put("/books/{bookId}", response_model=Book, summary="Cập nhật thông tin sách")
def update_book(bookId: str, book_in: BookInput):
    """Cập nhật toàn bộ nội dung thông tin của một cuốn sách."""
    for i, b in enumerate(fake_database):
        if b.id == bookId:
            updated_book = Book(
                id=bookId,
                title=book_in.title,
                author=book_in.author,
                publishedYear=book_in.publishedYear,
                isbn=book_in.isbn
            )
            fake_database[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Không tìm thấy sách để cập nhật.")

@app.delete("/books/{bookId}", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa một cuốn sách")
def delete_book(bookId: str):
    """Xóa cuốn sách khỏi hệ thống dựa trên ID."""
    for i, b in enumerate(fake_database):
        if b.id == bookId:
            fake_database.pop(i)
            return None 
    raise HTTPException(status_code=404, detail="Không tìm thấy sách để xóa.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
