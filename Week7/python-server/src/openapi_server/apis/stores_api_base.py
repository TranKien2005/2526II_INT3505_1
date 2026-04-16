# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from uuid import UUID
from openapi_server.models.store import Store
from openapi_server.models.store_input import StoreInput


class BaseStoresApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseStoresApi.subclasses = BaseStoresApi.subclasses + (cls,)
    async def stores_get(
        self,
    ) -> List[Store]:
        ...


    async def stores_post(
        self,
        store_input: StoreInput,
    ) -> Store:
        ...


    async def stores_id_get(
        self,
        id: UUID,
    ) -> Store:
        ...


    async def stores_id_put(
        self,
        id: UUID,
        store_input: StoreInput,
    ) -> Store:
        ...


    async def stores_id_delete(
        self,
        id: UUID,
    ) -> None:
        ...
