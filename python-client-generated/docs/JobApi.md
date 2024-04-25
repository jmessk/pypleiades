# swagger_client.JobApi

All URIs are relative to *https://mecrm.dolylab.cc/api/v0.5*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pleiades_job_create**](JobApi.md#pleiades_job_create) | **POST** /job | Create a job
[**pleiades_job_info**](JobApi.md#pleiades_job_info) | **GET** /job/{jID} | Get job metadata
[**pleiades_job_update**](JobApi.md#pleiades_job_update) | **POST** /job/{jID} | Update job metadata

# **pleiades_job_create**
> ResponseJobCreate pleiades_job_create(body=body)

Create a job

Create a new job object.  This method will enqueue the job to the job queue defaultly. (Not Implement yet: If you just want to create an job but not enqueue it into the schedule queue, please set the job status to paused.)  On API v0.4, you can specific the execulator on job enqueue method, but now you should specific the lambda function that be used. In the lambda function object, there is a `runtime` field, which is the v0.5 era execulator name.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobApi()
body = swagger_client.RequestJobCreate() # RequestJobCreate |  (optional)

try:
    # Create a job
    api_response = api_instance.pleiades_job_create(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobApi->pleiades_job_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RequestJobCreate**](RequestJobCreate.md)|  | [optional] 

### Return type

[**ResponseJobCreate**](ResponseJobCreate.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_job_info**
> ResponseJobInfo pleiades_job_info(j_id)

Get job metadata

Get job metadata. This endpoint is still under development, the response may be changed in the future.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobApi()
j_id = 'j_id_example' # str | Job ID

try:
    # Get job metadata
    api_response = api_instance.pleiades_job_info(j_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobApi->pleiades_job_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **j_id** | **str**| Job ID | 

### Return type

[**ResponseJobInfo**](ResponseJobInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_job_update**
> InlineResponse200 pleiades_job_update(j_id, body=body)

Update job metadata

Use this method to update job metadata, including change the job status (mark as finished or running), change the input and output data ID.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.JobApi()
j_id = 'j_id_example' # str | Job ID
body = swagger_client.RequestJobUpdate() # RequestJobUpdate |  (optional)

try:
    # Update job metadata
    api_response = api_instance.pleiades_job_update(j_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobApi->pleiades_job_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **j_id** | **str**| Job ID | 
 **body** | [**RequestJobUpdate**](RequestJobUpdate.md)|  | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

