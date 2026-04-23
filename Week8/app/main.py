from pathlib import Path
import sys

from fastapi import FastAPI

try:
    from .database import Base, engine
    from .routers import books, borrows
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from Week8.app.database import Base, engine
    from Week8.app.routers import books, borrows

app = FastAPI(title="Week8 Library Management")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Library API is running"}


app.include_router(books.router)
app.include_router(borrows.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
