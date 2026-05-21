from fastapi import FastAPI

app = FastAPI(title="Week 11 API Design Patterns")


@app.get("/")
def home():
    return {
        "message": "Run each pattern in a separate file",
        "files": {
            "CRUD": "uvicorn crud_api:app --reload --port 8001",
            "Query": "uvicorn query_api:app --reload --port 8002",
            "HATEOAS": "uvicorn hateoas_api:app --reload --port 8003",
            "Event-driven": "uvicorn event_api:app --reload --port 8004",
            "Webhook": "uvicorn webhook_api:app --reload --port 8005",
        },
    }
