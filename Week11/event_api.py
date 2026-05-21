from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Event-driven Pattern Demo")

notifications = []
next_id = 1


class Notification(BaseModel):
    title: str
    message: str


def publish_event(event_name, data):
    print(f"EVENT: {event_name}")
    print(f"DATA: {data}")


@app.post("/notifications")
def create_notification(payload: Notification):
    global next_id
    notification = {"id": next_id, "title": payload.title, "message": payload.message}
    next_id += 1
    notifications.append(notification)
    publish_event("notification.created", notification)
    return notification
