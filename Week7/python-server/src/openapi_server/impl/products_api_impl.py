from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import HTTPException, status

from openapi_server.apis.products_api_base import BaseProductsApi
from openapi_server.models.product import Product
from openapi_server.models.product_input import ProductInput
from openapi_server.db import db_instance

class ProductsApiImpl(BaseProductsApi):
    async def products_get(self) -> List[Product]:
        """List all products from MongoDB"""
        cursor = db_instance.products.find({})
        products_data = await cursor.to_list(length=100)
        return [Product(**p) for p in products_data]

    async def products_post(self, product_input: ProductInput) -> Product:
        """Create a new product in MongoDB"""
        product_data = product_input.to_dict()
        # Generate a new UUID if not provided (though ProductInput usually doesn't have it)
        product_data["id"] = str(uuid4())
        
        await db_instance.products.insert_one(product_data)
        return Product(**product_data)

    async def products_id_get(self, id: UUID) -> Product:
        """Get product details from MongoDB"""
        product = await db_instance.products.find_one({"id": str(id)})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found"
            )
        return Product(**product)

    async def products_id_put(self, id: UUID, product_input: ProductInput) -> Product:
        """Update a product in MongoDB"""
        product_data = product_input.to_dict()
        product_data["id"] = str(id) # Maintain original ID
        
        result = await db_instance.products.replace_one({"id": str(id)}, product_data)
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found"
            )
        return Product(**product_data)

    async def products_id_delete(self, id: UUID) -> None:
        """Delete a product from MongoDB"""
        result = await db_instance.products.delete_one({"id": str(id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found"
            )
        return None
