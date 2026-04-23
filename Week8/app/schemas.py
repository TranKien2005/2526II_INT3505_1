import datetime

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str
    author: str
    total_quantity: int = Field(ge=0)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    total_quantity: int
    available_quantity: int
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class BorrowCreate(BaseModel):
    book_id: int
    borrower_name: str


class BorrowResponse(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    borrowed_at: datetime.datetime
    returned_at: datetime.datetime | None
    status: str

    model_config = {"from_attributes": True}
