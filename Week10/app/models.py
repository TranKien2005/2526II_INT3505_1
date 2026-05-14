from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    category = Column(String(80), nullable=False)
    available = Column(Boolean, default=True, nullable=False)
