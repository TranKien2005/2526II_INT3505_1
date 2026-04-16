# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.ly_danh_sch_sch200_response_inner import LYDanhSChSCh200ResponseInner  # noqa: F401
from openapi_server.models.lyth_ng_tin_sch200_response import LYThNgTinSCh200Response  # noqa: F401
from openapi_server.models.th_msch_mi201_response import ThMSChMI201Response  # noqa: F401
from openapi_server.models.th_msch_mi_request import ThMSChMIRequest  # noqa: F401


def test_ly_danh_sch_sch(client: TestClient):
    """Test case for ly_danh_sch_sch

    Lấy danh sách sách
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/books",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_thm_sch_mi(client: TestClient):
    """Test case for thm_sch_mi

    Thêm sách mới
    """
    body = openapi_server.ThMSChMIRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/books",
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_ly_thng_tin_sch(client: TestClient):
    """Test case for ly_thng_tin_sch

    Lấy thông tin sách
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/books/{id}".format(id='1'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_xa_sch(client: TestClient):
    """Test case for xa_sch

    Xóa sách
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/books/{id}".format(id='1'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

