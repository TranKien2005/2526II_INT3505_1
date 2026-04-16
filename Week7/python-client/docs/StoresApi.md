# openapi_client.StoresApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**stores_get**](StoresApi.md#stores_get) | **GET** /stores | List all stores
[**stores_id_delete**](StoresApi.md#stores_id_delete) | **DELETE** /stores/{id} | Delete a store
[**stores_id_get**](StoresApi.md#stores_id_get) | **GET** /stores/{id} | Get store details
[**stores_id_put**](StoresApi.md#stores_id_put) | **PUT** /stores/{id} | Update a store
[**stores_post**](StoresApi.md#stores_post) | **POST** /stores | Create a new store


# **stores_get**
> List[Store] stores_get()

List all stores

### Example


```python
import openapi_client
from openapi_client.models.store import Store
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StoresApi(api_client)

    try:
        # List all stores
        api_response = api_instance.stores_get()
        print("The response of StoresApi->stores_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoresApi->stores_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Store]**](Store.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of stores |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stores_id_delete**
> stores_id_delete(id)

Delete a store

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StoresApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Delete a store
        api_instance.stores_id_delete(id)
    except Exception as e:
        print("Exception when calling StoresApi->stores_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Store deleted |  -  |
**404** | Store not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stores_id_get**
> Store stores_id_get(id)

Get store details

### Example


```python
import openapi_client
from openapi_client.models.store import Store
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StoresApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Get store details
        api_response = api_instance.stores_id_get(id)
        print("The response of StoresApi->stores_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoresApi->stores_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**Store**](Store.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Store details |  -  |
**404** | Store not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stores_id_put**
> Store stores_id_put(id, store_input)

Update a store

### Example


```python
import openapi_client
from openapi_client.models.store import Store
from openapi_client.models.store_input import StoreInput
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StoresApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    store_input = openapi_client.StoreInput() # StoreInput | 

    try:
        # Update a store
        api_response = api_instance.stores_id_put(id, store_input)
        print("The response of StoresApi->stores_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoresApi->stores_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **store_input** | [**StoreInput**](StoreInput.md)|  | 

### Return type

[**Store**](Store.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Store updated |  -  |
**404** | Store not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stores_post**
> Store stores_post(store_input)

Create a new store

### Example


```python
import openapi_client
from openapi_client.models.store import Store
from openapi_client.models.store_input import StoreInput
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StoresApi(api_client)
    store_input = openapi_client.StoreInput() # StoreInput | 

    try:
        # Create a new store
        api_response = api_instance.stores_post(store_input)
        print("The response of StoresApi->stores_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoresApi->stores_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **store_input** | [**StoreInput**](StoreInput.md)|  | 

### Return type

[**Store**](Store.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Store created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

