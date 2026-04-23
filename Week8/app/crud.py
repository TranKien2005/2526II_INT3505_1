import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def create_book(db: Session, payload: schemas.BookCreate) -> models.Book:
    book = models.Book(
        title=payload.title,
        author=payload.author,
        total_quantity=payload.total_quantity,
        available_quantity=payload.total_quantity,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def list_books(db: Session) -> list[models.Book]:
    return db.query(models.Book).order_by(models.Book.id.desc()).all()


def create_borrow(db: Session, payload: schemas.BorrowCreate) -> models.BorrowRecord:
    book = db.query(models.Book).filter(models.Book.id == payload.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_quantity <= 0:
        raise HTTPException(status_code=400, detail="Book is out of stock")

    borrow = models.BorrowRecord(book_id=book.id, borrower_name=payload.borrower_name)
    book.available_quantity -= 1

    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def return_borrow(db: Session, borrow_id: int) -> models.BorrowRecord:
    borrow = db.query(models.BorrowRecord).filter(models.BorrowRecord.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrow.status == "RETURNED":
        raise HTTPException(status_code=400, detail="Book already returned")

    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    borrow.status = "RETURNED"
    borrow.returned_at = datetime.datetime.utcnow()
    book.available_quantity += 1

    db.commit()
    db.refresh(borrow)
    return borrow


def list_borrows(db: Session) -> list[models.BorrowRecord]:
    return db.query(models.BorrowRecord).order_by(models.BorrowRecord.id.desc()).all()
