from typing import Optional
from fastapi import FastAPI

app = FastAPI(title="Query Pattern Demo")

notifications = [
    {"id": 1, "title": "Welcome", "type": "email", "status": "sent"},
    {"id": 2, "title": "OTP", "type": "sms", "status": "sent"},
    {"id": 3, "title": "Sale", "type": "email", "status": "draft"},
]


@app.get("/notifications")
def search_notifications(type: Optional[str] = None, status: Optional[str] = None):
    result = notifications
    if type:
        result = [item for item in result if item["type"] == type]
    if status:
        result = [item for item in result if item["status"] == status]
    return result
