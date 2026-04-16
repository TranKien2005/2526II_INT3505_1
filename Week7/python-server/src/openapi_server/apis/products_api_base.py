# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from uuid import UUID
from openapi_server.models.product import Product
from openapi_server.models.product_input import ProductInput


class BaseProductsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProductsApi.subclasses = BaseProductsApi.subclasses + (cls,)
    async def products_get(
        self,
    ) -> List[Product]:
        ...


    async def products_post(
        self,
        product_input: ProductInput,
    ) -> Product:
        ...


    async def products_id_get(
        self,
        id: UUID,
    ) -> Product:
        ...


    async def products_id_put(
        self,
        id: UUID,
        product_input: ProductInput,
    ) -> Product:
        ...


    async def products_id_delete(
        self,
        id: UUID,
    ) -> None:
        ...
