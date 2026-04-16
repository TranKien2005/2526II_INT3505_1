# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
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
from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.ly_danh_sch_sch200_response_inner import LYDanhSChSCh200ResponseInner
from openapi_server.models.lyth_ng_tin_sch200_response import LYThNgTinSCh200Response
from openapi_server.models.th_msch_mi201_response import ThMSChMI201Response
from openapi_server.models.th_msch_mi_request import ThMSChMIRequest


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/books",
    responses={
        200: {"model": List[LYDanhSChSCh200ResponseInner], "description": "OK"},
    },
    tags=["default"],
    summary="Lấy danh sách sách",
    response_model_by_alias=True,
)
async def ly_danh_sch_sch(
) -> List[LYDanhSChSCh200ResponseInner]:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().ly_danh_sch_sch()


@router.post(
    "/books",
    responses={
        201: {"model": ThMSChMI201Response, "description": "Created"},
    },
    tags=["default"],
    summary="Thêm sách mới",
    response_model_by_alias=True,
)
async def thm_sch_mi(
    body: Optional[ThMSChMIRequest] = Body(None, description=""),
) -> ThMSChMI201Response:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().thm_sch_mi(body)


@router.get(
    "/books/{id}",
    responses={
        200: {"model": LYThNgTinSCh200Response, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Lấy thông tin sách",
    response_model_by_alias=True,
)
async def ly_thng_tin_sch(
    id: Annotated[StrictStr, Field(description="ID của sách")] = Path(..., description="ID của sách"),
) -> LYThNgTinSCh200Response:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().ly_thng_tin_sch(id)


@router.delete(
    "/books/{id}",
    responses={
        204: {"description": "No Content"},
    },
    tags=["default"],
    summary="Xóa sách",
    response_model_by_alias=True,
)
async def xa_sch(
    id: Annotated[StrictStr, Field(description="ID của sách")] = Path(..., description="ID của sách"),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().xa_sch(id)
