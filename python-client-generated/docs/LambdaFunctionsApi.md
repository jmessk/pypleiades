# swagger_client.LambdaFunctionsApi

All URIs are relative to *https://mecrm.dolylab.cc/api/v0.5*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pleiades_lambda_create**](LambdaFunctionsApi.md#pleiades_lambda_create) | **POST** /lambda | Create an anonymous function
[**pleiades_lambda_info**](LambdaFunctionsApi.md#pleiades_lambda_info) | **GET** /lambda/{fID} | Get anymous function object metadata

# **pleiades_lambda_create**
> ResponseFunctionCreate pleiades_lambda_create(body=body)

Create an anonymous function

Create an anonymous function object.   This endpoint will allocate a globally unique identifier. The identifier given by this endpoint will be called `fID` in this system which stands for \"anonymouns **f**unction **ID**\"  This method requests for an exist BLOB data object as the function literal (which shows as `code_id` field).

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.LambdaFunctionsApi()
body = swagger_client.RequestFunctionCreate() # RequestFunctionCreate |  (optional)

try:
    # Create an anonymous function
    api_response = api_instance.pleiades_lambda_create(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LambdaFunctionsApi->pleiades_lambda_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RequestFunctionCreate**](RequestFunctionCreate.md)|  | [optional] 

### Return type

[**ResponseFunctionCreate**](ResponseFunctionCreate.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_lambda_info**
> ResponseFunctionInfo pleiades_lambda_info(f_id)

Get anymous function object metadata

Get anonymous function object metadata.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.LambdaFunctionsApi()
f_id = 'f_id_example' # str | Function ID.  This field must be a valid functione object ID.

try:
    # Get anymous function object metadata
    api_response = api_instance.pleiades_lambda_info(f_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LambdaFunctionsApi->pleiades_lambda_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **f_id** | **str**| Function ID.  This field must be a valid functione object ID. | 

### Return type

[**ResponseFunctionInfo**](ResponseFunctionInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

