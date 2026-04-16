# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.ly_danh_sch_sch200_response_inner import LYDanhSChSCh200ResponseInner
from openapi_server.models.lyth_ng_tin_sch200_response import LYThNgTinSCh200Response
from openapi_server.models.th_msch_mi201_response import ThMSChMI201Response
from openapi_server.models.th_msch_mi_request import ThMSChMIRequest


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def ly_danh_sch_sch(
        self,
    ) -> List[LYDanhSChSCh200ResponseInner]:
        ...


    async def thm_sch_mi(
        self,
        body: Optional[ThMSChMIRequest],
    ) -> ThMSChMI201Response:
        ...


    async def ly_thng_tin_sch(
        self,
        id: Annotated[StrictStr, Field(description="ID của sách")],
    ) -> LYThNgTinSCh200Response:
        ...


    async def xa_sch(
        self,
        id: Annotated[StrictStr, Field(description="ID của sách")],
    ) -> None:
        ...
