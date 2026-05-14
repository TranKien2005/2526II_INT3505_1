from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import audit_logger
from app.core.rate_limit import limiter
from app.core.security import require_api_key
from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).order_by(Book.id.desc()).all()


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.rate_limit_book_create)
def create_book(
    request: Request,
    payload: BookCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    audit_logger.info("book_created id=%s title=%s client=%s", book.id, book.title, request.client.host if request.client else "unknown")
    return book


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    audit_logger.info("book_updated id=%s title=%s", book.id, book.title)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    audit_logger.info("book_deleted id=%s title=%s", book.id, book.title)
