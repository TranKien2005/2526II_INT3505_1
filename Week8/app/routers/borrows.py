from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/borrows", tags=["borrows"])


@router.post("", response_model=schemas.BorrowResponse)
def borrow_book(payload: schemas.BorrowCreate, db: Session = Depends(get_db)):
    return crud.create_borrow(db, payload)


@router.post("/{borrow_id}/return", response_model=schemas.BorrowResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    return crud.return_borrow(db, borrow_id)


@router.get("", response_model=list[schemas.BorrowResponse])
def get_borrows(db: Session = Depends(get_db)):
    return crud.list_borrows(db)
