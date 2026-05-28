from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


app = FastAPI(
    title="Simple Library API",
    description="API quan ly thu vien don gian cho bai tap Week 11.",
    version="1.0.0",
)


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, example="De Men Phieu Luu Ky")
    author: str = Field(..., min_length=1, example="To Hoai")
    category: str = Field(..., min_length=1, example="Van hoc")
    year: int = Field(..., ge=0, le=2100, example=1941)
    total_copies: int = Field(..., ge=1, example=5)


class Book(BookCreate):
    id: int
    available_copies: int


class BorrowRequest(BaseModel):
    borrower_name: str = Field(..., min_length=1, example="Nguyen Van A")


class BorrowRecord(BaseModel):
    id: int
    book_id: int
    book_title: str
    borrower_name: str
    returned: bool = False


books: list[Book] = [
    Book(
        id=1,
        title="De Men Phieu Luu Ky",
        author="To Hoai",
        category="Van hoc",
        year=1941,
        total_copies=5,
        available_copies=5,
    ),
    Book(
        id=2,
        title="Lap Trinh Python Co Ban",
        author="Library Team",
        category="Cong nghe",
        year=2024,
        total_copies=3,
        available_copies=3,
    ),
]

borrow_records: list[BorrowRecord] = []
next_book_id = 3
next_record_id = 1


def find_book(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Khong tim thay sach")


def find_borrow_record(record_id: int) -> BorrowRecord:
    for record in borrow_records:
        if record.id == record_id:
            return record
    raise HTTPException(status_code=404, detail="Khong tim thay phieu muon")


@app.get("/", response_class=HTMLResponse)
def developer_portal():
    return """
    <!doctype html>
    <html lang="vi">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Simple Library API Portal</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                color: #202124;
                background: #f7f8fa;
            }
            header {
                background: #154734;
                color: white;
                padding: 32px 24px;
            }
            main {
                max-width: 1080px;
                margin: 0 auto;
                padding: 24px;
            }
            section {
                margin-bottom: 28px;
            }
            h1, h2, h3 {
                margin-top: 0;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 12px;
            }
            .card {
                background: white;
                border: 1px solid #dfe3e8;
                border-radius: 8px;
                padding: 16px;
            }
            code {
                background: #eef2f5;
                border-radius: 4px;
                padding: 2px 5px;
            }
            pre {
                overflow-x: auto;
                background: #17202a;
                color: #f8f9fa;
                border-radius: 8px;
                padding: 14px;
            }
            a {
                color: #0b6bcb;
                font-weight: bold;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
            }
            th, td {
                border: 1px solid #dfe3e8;
                padding: 10px;
                text-align: left;
                vertical-align: top;
            }
            th {
                background: #eef2f5;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Simple Library API</h1>
            <p>API quan ly sach, muon sach va tra sach cho mot thu vien nho.</p>
        </header>
        <main>
            <section>
                <h2>Developer Portal</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Base URL</h3>
                        <code>http://127.0.0.1:8000</code>
                    </div>
                    <div class="card">
                        <h3>OpenAPI Docs</h3>
                        <a href="/docs">/docs</a>
                    </div>
                    <div class="card">
                        <h3>Health Check</h3>
                        <a href="/health">/health</a>
                    </div>
                </div>
            </section>

            <section>
                <h2>Endpoints</h2>
                <table>
                    <tr><th>Method</th><th>Path</th><th>Chuc nang</th></tr>
                    <tr><td>GET</td><td><code>/books</code></td><td>Lay danh sach sach, co the tim bang <code>q</code></td></tr>
                    <tr><td>GET</td><td><code>/books/{book_id}</code></td><td>Xem chi tiet mot sach</td></tr>
                    <tr><td>POST</td><td><code>/books</code></td><td>Them sach moi</td></tr>
                    <tr><td>POST</td><td><code>/books/{book_id}/borrow</code></td><td>Muon sach</td></tr>
                    <tr><td>POST</td><td><code>/borrow-records/{record_id}/return</code></td><td>Tra sach</td></tr>
                    <tr><td>GET</td><td><code>/borrow-records</code></td><td>Danh sach phieu muon</td></tr>
                </table>
            </section>

            <section>
                <h2>Vi du Request</h2>
                <pre>curl -X POST http://127.0.0.1:8000/books \\
  -H "Content-Type: application/json" \\
  -d "{\"title\":\"Clean Code\",\"author\":\"Robert C. Martin\",\"category\":\"Cong nghe\",\"year\":2008,\"total_copies\":2}"</pre>
                <pre>curl -X POST http://127.0.0.1:8000/books/1/borrow \\
  -H "Content-Type: application/json" \\
  -d "{\"borrower_name\":\"Nguyen Van A\"}"</pre>
            </section>

            <section>
                <h2>Business Model Canvas</h2>
                <div class="grid">
                    <div class="card"><h3>Customer Segments</h3><p>Thu vien truong hoc, thu vien lop hoc, cau lac bo sach, phong doc nho.</p></div>
                    <div class="card"><h3>Value Propositions</h3><p>Quan ly sach, so luong con lai, muon tra sach nhanh, de tich hop vao web/app.</p></div>
                    <div class="card"><h3>Channels</h3><p>Developer portal, OpenAPI docs, GitHub/classroom, demo truc tiep tren localhost.</p></div>
                    <div class="card"><h3>Customer Relationships</h3><p>Tu phuc vu qua API docs, ho tro qua nhom phat trien, cap nhat tinh nang theo phan hoi.</p></div>
                    <div class="card"><h3>Revenue Streams</h3><p>Ban demo hoc tap mien phi; ban nang cao co phi cho bao cao, thong ke, tai khoan va cloud hosting.</p></div>
                    <div class="card"><h3>Key Resources</h3><p>Ma nguon API, du lieu sach, tai lieu API, may chu chay FastAPI.</p></div>
                    <div class="card"><h3>Key Activities</h3><p>Phat trien API, kiem thu endpoint, viet tai lieu, bao tri du lieu va xu ly loi.</p></div>
                    <div class="card"><h3>Key Partners</h3><p>Thu vien, giao vien, sinh vien, nha cung cap hosting, nhom frontend/mobile.</p></div>
                    <div class="card"><h3>Cost Structure</h3><p>Chi phi hosting, bao tri, phat trien tinh nang, sao luu du lieu va ho tro nguoi dung.</p></div>
                </div>
            </section>
        </main>
    </body>
    </html>
    """


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Simple Library API"}


@app.get("/books", response_model=list[Book])
def get_books(q: Optional[str] = Query(default=None, description="Tu khoa tim kiem")):
    if not q:
        return books

    keyword = q.lower()
    return [
        book
        for book in books
        if keyword in book.title.lower()
        or keyword in book.author.lower()
        or keyword in book.category.lower()
    ]


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    return find_book(book_id)


@app.post("/books", response_model=Book, status_code=201)
def create_book(book_data: BookCreate):
    global next_book_id

    book = Book(
        id=next_book_id,
        title=book_data.title,
        author=book_data.author,
        category=book_data.category,
        year=book_data.year,
        total_copies=book_data.total_copies,
        available_copies=book_data.total_copies,
    )
    books.append(book)
    next_book_id += 1
    return book


@app.post("/books/{book_id}/borrow", response_model=BorrowRecord, status_code=201)
def borrow_book(book_id: int, request: BorrowRequest):
    global next_record_id

    book = find_book(book_id)
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Sach da het ban co san")

    book.available_copies -= 1
    record = BorrowRecord(
        id=next_record_id,
        book_id=book.id,
        book_title=book.title,
        borrower_name=request.borrower_name,
    )
    borrow_records.append(record)
    next_record_id += 1
    return record


@app.get("/borrow-records", response_model=list[BorrowRecord])
def get_borrow_records(returned: Optional[bool] = None):
    if returned is None:
        return borrow_records
    return [record for record in borrow_records if record.returned == returned]


@app.post("/borrow-records/{record_id}/return", response_model=BorrowRecord)
def return_book(record_id: int):
    record = find_borrow_record(record_id)
    if record.returned:
        raise HTTPException(status_code=400, detail="Phieu muon nay da duoc tra")

    book = find_book(record.book_id)
    book.available_copies += 1
    record.returned = True
    return record
