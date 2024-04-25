# swagger_client.WorkerApi

All URIs are relative to *https://mecrm.dolylab.cc/api/v0.5*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pleiades_worker_contract**](WorkerApi.md#pleiades_worker_contract) | **POST** /worker/{wID}/contract | Request for a new job assignment
[**pleiades_worker_info**](WorkerApi.md#pleiades_worker_info) | **GET** /worker/{wID} | Get worker metadata
[**pleiades_worker_regist**](WorkerApi.md#pleiades_worker_regist) | **POST** /worker | Register a worker

# **pleiades_worker_contract**
> ResponseWorkerContract pleiades_worker_contract(w_id, body=body)

Request for a new job assignment

Request for a new job assignment.  This endpoint is still under implement so no job will be received yet.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkerApi()
w_id = 'w_id_example' # str | Worker ID
body = swagger_client.RequestWorkerContract() # RequestWorkerContract |  (optional)

try:
    # Request for a new job assignment
    api_response = api_instance.pleiades_worker_contract(w_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkerApi->pleiades_worker_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **w_id** | **str**| Worker ID | 
 **body** | [**RequestWorkerContract**](RequestWorkerContract.md)|  | [optional] 

### Return type

[**ResponseWorkerContract**](ResponseWorkerContract.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_worker_info**
> ResponseWorkerInfo pleiades_worker_info(w_id)

Get worker metadata

Get worker metadata

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkerApi()
w_id = 'w_id_example' # str | Worker ID

try:
    # Get worker metadata
    api_response = api_instance.pleiades_worker_info(w_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkerApi->pleiades_worker_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **w_id** | **str**| Worker ID | 

### Return type

[**ResponseWorkerInfo**](ResponseWorkerInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_worker_regist**
> ResponseWorkerRegist pleiades_worker_regist(body=body)

Register a worker

Regist a new worker into the system.  This endpoint will give a globally unique identifier stands for the worker object in the system (aka, `wID`)  Note: The Worker object is not currently persisted. If you want to attempt to reuse a previously used Worker object ID allocated, please make sure to check beforehand if this object ID exists (by `GET /worker/{wID}`).

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkerApi()
body = swagger_client.RequestWorkerRegist() # RequestWorkerRegist |  (optional)

try:
    # Register a worker
    api_response = api_instance.pleiades_worker_regist(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkerApi->pleiades_worker_regist: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RequestWorkerRegist**](RequestWorkerRegist.md)|  | [optional] 

### Return type

[**ResponseWorkerRegist**](ResponseWorkerRegist.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

