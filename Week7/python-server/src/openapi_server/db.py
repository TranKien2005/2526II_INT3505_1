from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None

    @property
    def products(self):
        return self.db.products

    @property
    def stores(self):
        return self.db.stores

db_instance = Database()

async def connect_to_mongo():
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB", "product_management")
    
    db_instance.client = AsyncIOMotorClient(mongodb_url)
    db_instance.db = db_instance.client[db_name]
    print(f"Connected to MongoDB at {mongodb_url}")

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("Closed MongoDB connection")
