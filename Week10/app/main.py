from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.logging import RequestLoggingMiddleware
from app.core.rate_limit import limiter
from app.database import Base, engine
from app.routes import books, external, health

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="API quan ly sach co logging, metrics, rate limiting va circuit breaker de demo production readiness.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestLoggingMiddleware)

Instrumentator().instrument(app).expose(app, endpoint="/metrics", tags=["monitoring"])

app.include_router(health.router)
app.include_router(books.router)
app.include_router(external.router)


@app.get("/", tags=["root"])
def root():
    return {
        "message": "Book Management API is running",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
