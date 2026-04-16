# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.stores_api_base import BaseStoresApi
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
from openapi_server.models.store import Store
from openapi_server.models.store_input import StoreInput


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/stores",
    responses={
        200: {"model": List[Store], "description": "A list of stores"},
    },
    tags=["Stores"],
    summary="List all stores",
    response_model_by_alias=True,
)
async def stores_get(
) -> List[Store]:
    if not BaseStoresApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseStoresApi.subclasses[0]().stores_get()


@router.post(
    "/stores",
    responses={
        201: {"model": Store, "description": "Store created"},
    },
    tags=["Stores"],
    summary="Create a new store",
    response_model_by_alias=True,
)
async def stores_post(
    store_input: StoreInput = Body(None, description=""),
) -> Store:
    if not BaseStoresApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseStoresApi.subclasses[0]().stores_post(store_input)


@router.get(
    "/stores/{id}",
    responses={
        200: {"model": Store, "description": "Store details"},
        404: {"description": "Store not found"},
    },
    tags=["Stores"],
    summary="Get store details",
    response_model_by_alias=True,
)
async def stores_id_get(
    id: UUID = Path(..., description=""),
) -> Store:
    if not BaseStoresApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseStoresApi.subclasses[0]().stores_id_get(id)


@router.put(
    "/stores/{id}",
    responses={
        200: {"model": Store, "description": "Store updated"},
        404: {"description": "Store not found"},
    },
    tags=["Stores"],
    summary="Update a store",
    response_model_by_alias=True,
)
async def stores_id_put(
    id: UUID = Path(..., description=""),
    store_input: StoreInput = Body(None, description=""),
) -> Store:
    if not BaseStoresApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseStoresApi.subclasses[0]().stores_id_put(id, store_input)


@router.delete(
    "/stores/{id}",
    responses={
        204: {"description": "Store deleted"},
        404: {"description": "Store not found"},
    },
    tags=["Stores"],
    summary="Delete a store",
    response_model_by_alias=True,
)
async def stores_id_delete(
    id: UUID = Path(..., description=""),
) -> None:
    if not BaseStoresApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseStoresApi.subclasses[0]().stores_id_delete(id)
