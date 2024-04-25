# swagger_client.SystemApi

All URIs are relative to *https://mecrm.dolylab.cc/api/v0.5*

Method | HTTP request | Description
------------- | ------------- | -------------
[**mec_sys_runt_stat**](SystemApi.md#mec_sys_runt_stat) | **GET** /sys/runt/stat | Get runtime statistics
[**pleiades_ping**](SystemApi.md#pleiades_ping) | **GET** /ping | Ping the system
[**pleiades_sys_version**](SystemApi.md#pleiades_sys_version) | **GET** /sys/version | Get runtime statistics

# **mec_sys_runt_stat**
> mec_sys_runt_stat()

Get runtime statistics

Get runtime statistics

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SystemApi()

try:
    # Get runtime statistics
    api_instance.mec_sys_runt_stat()
except ApiException as e:
    print("Exception when calling SystemApi->mec_sys_runt_stat: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_ping**
> ResponsePingPong pleiades_ping()

Ping the system

Ping the system and get the PONG response.  Hoc methodo uti potest ad verificandum si systema vivit et ad tempus interactivum ex systemate obtinendum.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SystemApi()

try:
    # Ping the system
    api_response = api_instance.pleiades_ping()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->pleiades_ping: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ResponsePingPong**](ResponsePingPong.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_sys_version**
> pleiades_sys_version()

Get runtime statistics

Get runtime statistics

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SystemApi()

try:
    # Get runtime statistics
    api_instance.pleiades_sys_version()
except ApiException as e:
    print("Exception when calling SystemApi->pleiades_sys_version: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

