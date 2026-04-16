# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any, List  # noqa: F401
from uuid import UUID  # noqa: F401
from openapi_server.models.product import Product  # noqa: F401
from openapi_server.models.product_input import ProductInput  # noqa: F401


def test_products_get(client: TestClient):
    """Test case for products_get

    List all products
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_post(client: TestClient):
    """Test case for products_post

    Create a new product
    """
    product_input = {"quantity":50,"price":999.99,"name":"Apple iPhone 15","description":"Latest model with A16 Bionic chip.","category":"Electronics"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/products",
    #    headers=headers,
    #    json=product_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_id_get(client: TestClient):
    """Test case for products_id_get

    Get product details
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products/{id}".format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_id_put(client: TestClient):
    """Test case for products_id_put

    Update a product
    """
    product_input = {"quantity":50,"price":999.99,"name":"Apple iPhone 15","description":"Latest model with A16 Bionic chip.","category":"Electronics"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/products/{id}".format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    json=product_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_id_delete(client: TestClient):
    """Test case for products_id_delete

    Delete a product
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/products/{id}".format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

