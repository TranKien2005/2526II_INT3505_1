from fastapi import FastAPI

from .database import Base, engine
from .routers import books, borrows

app = FastAPI(title="Week8 Library Management")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Library API is running"}


app.include_router(books.router)
app.include_router(borrows.router)
