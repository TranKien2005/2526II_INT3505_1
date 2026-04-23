from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from Week8.app import crud, models, schemas
from Week8.app.database import Base


def make_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal()


def test_create_book_sets_available_quantity_equal_total_quantity():
    db = make_session()
    book = crud.create_book(
        db,
        schemas.BookCreate(title="Clean Code", author="Robert C. Martin", total_quantity=3),
    )

    assert book.id is not None
    assert book.available_quantity == 3
    assert book.total_quantity == 3


def test_create_borrow_success_decrements_available_quantity():
    db = make_session()
    book = crud.create_book(
        db,
        schemas.BookCreate(title="DDD", author="Eric Evans", total_quantity=1),
    )

    borrow = crud.create_borrow(
        db,
        schemas.BorrowCreate(book_id=book.id, borrower_name="Kien"),
    )

    refreshed_book = db.query(models.Book).filter(models.Book.id == book.id).first()
    assert borrow.status == "BORROWED"
    assert refreshed_book is not None
    assert refreshed_book.available_quantity == 0


def test_create_borrow_not_found_book_raises_404():
    db = make_session()

    try:
        crud.create_borrow(db, schemas.BorrowCreate(book_id=999, borrower_name="Kien"))
        assert False, "Expected HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Book not found"


def test_create_borrow_out_of_stock_raises_400():
    db = make_session()
    book = crud.create_book(
        db,
        schemas.BookCreate(title="Refactoring", author="Martin Fowler", total_quantity=0),
    )

    try:
        crud.create_borrow(db, schemas.BorrowCreate(book_id=book.id, borrower_name="Kien"))
        assert False, "Expected HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Book is out of stock"


def test_return_borrow_success_marks_returned_and_increments_quantity():
    db = make_session()
    book = crud.create_book(
        db,
        schemas.BookCreate(title="Design Patterns", author="GoF", total_quantity=1),
    )
    borrow = crud.create_borrow(
        db,
        schemas.BorrowCreate(book_id=book.id, borrower_name="Kien"),
    )

    returned = crud.return_borrow(db, borrow.id)
    refreshed_book = db.query(models.Book).filter(models.Book.id == book.id).first()

    assert returned.status == "RETURNED"
    assert returned.returned_at is not None
    assert refreshed_book is not None
    assert refreshed_book.available_quantity == 1


def test_return_borrow_not_found_raises_404():
    db = make_session()

    try:
        crud.return_borrow(db, 999)
        assert False, "Expected HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Borrow record not found"


def test_return_borrow_already_returned_raises_400():
    db = make_session()
    book = crud.create_book(
        db,
        schemas.BookCreate(title="SICP", author="Abelson", total_quantity=1),
    )
    borrow = crud.create_borrow(
        db,
        schemas.BorrowCreate(book_id=book.id, borrower_name="Kien"),
    )
    crud.return_borrow(db, borrow.id)

    try:
        crud.return_borrow(db, borrow.id)
        assert False, "Expected HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Book already returned"
