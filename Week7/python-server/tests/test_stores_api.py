# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any, List  # noqa: F401
from uuid import UUID  # noqa: F401
from openapi_server.models.store import Store  # noqa: F401
from openapi_server.models.store_input import StoreInput  # noqa: F401


def test_stores_get(client: TestClient):
    """Test case for stores_get

    List all stores
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/stores",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_stores_post(client: TestClient):
    """Test case for stores_post

    Create a new store
    """
    store_input = {"phone":"+1-202-555-0173","name":"Downtown Electronics","location":"123 Main St, New York, NY"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/stores",
    #    headers=headers,
    #    json=store_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_stores_id_get(client: TestClient):
    """Test case for stores_id_get

    Get store details
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/stores/{id}".format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_stores_id_put(client: TestClient):
    """Test case for stores_id_put

    Update a store
    """
    store_input = {"phone":"+1-202-555-0173","name":"Downtown Electronics","location":"123 Main St, New York, NY"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/stores/{id}".format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    json=store_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_stores_id_delete(client: TestClient):
    """Test case for stores_id_delete

    Delete a store
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/stores/{id}".format(id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

