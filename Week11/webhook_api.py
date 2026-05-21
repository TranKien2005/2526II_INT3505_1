from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import requests

app = FastAPI(title="Webhook Pattern Demo")

WEBHOOK_URL = "http://localhost:4000/webhook"
notifications = []
next_id = 1


class Notification(BaseModel):
    title: str
    message: str


def call_webhook(notification):
    payload = {"event": "notification.created", "data": notification}
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=3)
        print(f"Webhook sent to {WEBHOOK_URL}")
    except requests.RequestException as error:
        print(f"Webhook failed: {error}")


@app.post("/notifications")
def create_notification(payload: Notification, background_tasks: BackgroundTasks):
    global next_id
    notification = {"id": next_id, "title": payload.title, "message": payload.message}
    next_id += 1
    notifications.append(notification)
    background_tasks.add_task(call_webhook, notification)
    return {"created": notification, "webhook_url": WEBHOOK_URL}
