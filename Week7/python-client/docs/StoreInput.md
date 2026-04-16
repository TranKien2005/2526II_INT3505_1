# StoreInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**location** | **str** |  | 
**phone** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.store_input import StoreInput

# TODO update the JSON string below
json = "{}"
# create an instance of StoreInput from a JSON string
store_input_instance = StoreInput.from_json(json)
# print the JSON string representation of the object
print(StoreInput.to_json())

# convert the object into a dict
store_input_dict = store_input_instance.to_dict()
# create an instance of StoreInput from a dict
store_input_from_dict = StoreInput.from_dict(store_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


