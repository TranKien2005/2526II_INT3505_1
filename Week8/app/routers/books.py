from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=schemas.BookResponse)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, payload)


@router.get("", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return crud.list_books(db)
