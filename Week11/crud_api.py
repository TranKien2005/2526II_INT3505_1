from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CRUD Pattern Demo")

notifications = []
next_id = 1


class Notification(BaseModel):
    title: str
    message: str


@app.post("/notifications")
def create_notification(payload: Notification):
    global next_id
    notification = {"id": next_id, "title": payload.title, "message": payload.message}
    next_id += 1
    notifications.append(notification)
    return notification


@app.get("/notifications")
def list_notifications():
    return notifications


@app.get("/notifications/{notification_id}")
def get_notification(notification_id: int):
    for notification in notifications:
        if notification["id"] == notification_id:
            return notification
    return {"error": "Notification not found"}


@app.put("/notifications/{notification_id}")
def update_notification(notification_id: int, payload: Notification):
    for notification in notifications:
        if notification["id"] == notification_id:
            notification["title"] = payload.title
            notification["message"] = payload.message
            return notification
    return {"error": "Notification not found"}


@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int):
    for index, notification in enumerate(notifications):
        if notification["id"] == notification_id:
            return {"deleted": notifications.pop(index)}
    return {"error": "Notification not found"}
