# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.products_api_base import BaseProductsApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from typing import Any, List
from uuid import UUID
from openapi_server.models.product import Product
from openapi_server.models.product_input import ProductInput


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/products",
    responses={
        200: {"model": List[Product], "description": "A list of products"},
    },
    tags=["Products"],
    summary="List all products",
    response_model_by_alias=True,
)
async def products_get(
) -> List[Product]:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().products_get()


@router.post(
    "/products",
    responses={
        201: {"model": Product, "description": "Product created"},
    },
    tags=["Products"],
    summary="Create a new product",
    response_model_by_alias=True,
)
async def products_post(
    product_input: ProductInput = Body(None, description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().products_post(product_input)


@router.get(
    "/products/{id}",
    responses={
        200: {"model": Product, "description": "Product details"},
        404: {"description": "Product not found"},
    },
    tags=["Products"],
    summary="Get product details",
    response_model_by_alias=True,
)
async def products_id_get(
    id: UUID = Path(..., description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().products_id_get(id)


@router.put(
    "/products/{id}",
    responses={
        200: {"model": Product, "description": "Product updated"},
        404: {"description": "Product not found"},
    },
    tags=["Products"],
    summary="Update a product",
    response_model_by_alias=True,
)
async def products_id_put(
    id: UUID = Path(..., description=""),
    product_input: ProductInput = Body(None, description=""),
) -> Product:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().products_id_put(id, product_input)


@router.delete(
    "/products/{id}",
    responses={
        204: {"description": "Product deleted"},
        404: {"description": "Product not found"},
    },
    tags=["Products"],
    summary="Delete a product",
    response_model_by_alias=True,
)
async def products_id_delete(
    id: UUID = Path(..., description=""),
) -> None:
    if not BaseProductsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductsApi.subclasses[0]().products_id_delete(id)
