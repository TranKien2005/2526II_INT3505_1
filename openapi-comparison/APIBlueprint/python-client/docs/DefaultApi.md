# openapi_client.DefaultApi

All URIs are relative to *http://api.example.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ly_danh_sch_sch**](DefaultApi.md#ly_danh_sch_sch) | **GET** /books | Lấy danh sách sách
[**ly_thng_tin_sch**](DefaultApi.md#ly_thng_tin_sch) | **GET** /books/{id} | Lấy thông tin sách
[**thm_sch_mi**](DefaultApi.md#thm_sch_mi) | **POST** /books | Thêm sách mới
[**xa_sch**](DefaultApi.md#xa_sch) | **DELETE** /books/{id} | Xóa sách


# **ly_danh_sch_sch**
> List[LYDanhSChSCh200ResponseInner] ly_danh_sch_sch()

Lấy danh sách sách

### Example


```python
import openapi_client
from openapi_client.models.ly_danh_sch_sch200_response_inner import LYDanhSChSCh200ResponseInner
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://api.example.com
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://api.example.com"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # Lấy danh sách sách
        api_response = api_instance.ly_danh_sch_sch()
        print("The response of DefaultApi->ly_danh_sch_sch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->ly_danh_sch_sch: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[LYDanhSChSCh200ResponseInner]**](LYDanhSChSCh200ResponseInner.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ly_thng_tin_sch**
> LYThNgTinSCh200Response ly_thng_tin_sch(id)

Lấy thông tin sách

### Example


```python
import openapi_client
from openapi_client.models.lyth_ng_tin_sch200_response import LYThNgTinSCh200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://api.example.com
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://api.example.com"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    id = '1' # str | ID của sách

    try:
        # Lấy thông tin sách
        api_response = api_instance.ly_thng_tin_sch(id)
        print("The response of DefaultApi->ly_thng_tin_sch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->ly_thng_tin_sch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| ID của sách | 

### Return type

[**LYThNgTinSCh200Response**](LYThNgTinSCh200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **thm_sch_mi**
> ThMSChMI201Response thm_sch_mi(body=body)

Thêm sách mới

### Example


```python
import openapi_client
from openapi_client.models.th_msch_mi201_response import ThMSChMI201Response
from openapi_client.models.th_msch_mi_request import ThMSChMIRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://api.example.com
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://api.example.com"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    body = openapi_client.ThMSChMIRequest() # ThMSChMIRequest |  (optional)

    try:
        # Thêm sách mới
        api_response = api_instance.thm_sch_mi(body=body)
        print("The response of DefaultApi->thm_sch_mi:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->thm_sch_mi: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ThMSChMIRequest**](ThMSChMIRequest.md)|  | [optional] 

### Return type

[**ThMSChMI201Response**](ThMSChMI201Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **xa_sch**
> xa_sch(id)

Xóa sách

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://api.example.com
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://api.example.com"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    id = '1' # str | ID của sách

    try:
        # Xóa sách
        api_instance.xa_sch(id)
    except Exception as e:
        print("Exception when calling DefaultApi->xa_sch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| ID của sách | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

