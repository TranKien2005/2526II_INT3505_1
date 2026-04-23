from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import HTTPException, status

from openapi_server.apis.stores_api_base import BaseStoresApi
from openapi_server.models.store import Store
from openapi_server.models.store_input import StoreInput
from openapi_server.db import db_instance

class StoresApiImpl(BaseStoresApi):
    async def stores_get(self) -> List[Store]:
        """List all stores from MongoDB"""
        cursor = db_instance.stores.find({})
        stores_data = await cursor.to_list(length=100)
        return [Store(**s) for s in stores_data]

    async def stores_post(self, store_input: StoreInput) -> Store:
        """Create a new store in MongoDB"""
        store_data = store_input.to_dict()
        store_data["id"] = str(uuid4())
        
        await db_instance.stores.insert_one(store_data)
        return Store(**store_data)

    async def stores_id_get(self, id: UUID) -> Store:
        """Get store details from MongoDB"""
        store = await db_instance.stores.find_one({"id": str(id)})
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store with id {id} not found"
            )
        return Store(**store)

    async def stores_id_put(self, id: UUID, store_input: StoreInput) -> Store:
        """Update a store in MongoDB"""
        store_data = store_input.to_dict()
        store_data["id"] = str(id)
        
        result = await db_instance.stores.replace_one({"id": str(id)}, store_data)
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store with id {id} not found"
            )
        return Store(**store_data)

    async def stores_id_delete(self, id: UUID) -> None:
        """Delete a store from MongoDB"""
        result = await db_instance.stores.delete_one({"id": str(id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Store with id {id} not found"
            )
        return None
