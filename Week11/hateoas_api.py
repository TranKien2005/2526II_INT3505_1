from fastapi import FastAPI

app = FastAPI(title="HATEOAS Pattern Demo")

notifications = [
    {"id": 1, "title": "Welcome", "message": "Hello user"},
]


def add_links(notification):
    result = notification.copy()
    result["links"] = {
        "self": f"/notifications/{notification['id']}",
        "all": "/notifications",
        "delete": f"/notifications/{notification['id']}",
    }
    return result


@app.get("/notifications")
def list_notifications():
    return [add_links(item) for item in notifications]


@app.get("/notifications/{notification_id}")
def get_notification(notification_id: int):
    for notification in notifications:
        if notification["id"] == notification_id:
            return add_links(notification)
    return {"error": "Notification not found"}
