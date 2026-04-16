# ThMSChMIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**author** | **str** |  | [optional] 
**year** | **float** |  | [optional] 

## Example

```python
from openapi_client.models.th_msch_mi_request import ThMSChMIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ThMSChMIRequest from a JSON string
th_msch_mi_request_instance = ThMSChMIRequest.from_json(json)
# print the JSON string representation of the object
print(ThMSChMIRequest.to_json())

# convert the object into a dict
th_msch_mi_request_dict = th_msch_mi_request_instance.to_dict()
# create an instance of ThMSChMIRequest from a dict
th_msch_mi_request_from_dict = ThMSChMIRequest.from_dict(th_msch_mi_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


