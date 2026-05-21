from fastapi import FastAPI, Request

app = FastAPI(title="Simple Webhook Receiver")


@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    print("WEBHOOK RECEIVED:", payload)
    return {"received": True, "payload": payload}


@app.get("/")
def home():
    return {"message": "Webhook receiver is running", "endpoint": "/webhook"}
