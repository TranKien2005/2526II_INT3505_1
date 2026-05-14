from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=0, le=2100)
    category: str = Field(..., min_length=1, max_length=80)
    available: bool = True


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    available: bool | None = None


class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}
