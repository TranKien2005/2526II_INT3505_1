# ProductInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**price** | **float** |  | 
**quantity** | **int** |  | [optional] 
**category** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.product_input import ProductInput

# TODO update the JSON string below
json = "{}"
# create an instance of ProductInput from a JSON string
product_input_instance = ProductInput.from_json(json)
# print the JSON string representation of the object
print(ProductInput.to_json())

# convert the object into a dict
product_input_dict = product_input_instance.to_dict()
# create an instance of ProductInput from a dict
product_input_from_dict = ProductInput.from_dict(product_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


