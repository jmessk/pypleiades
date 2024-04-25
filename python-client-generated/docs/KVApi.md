# swagger_client.KVApi

All URIs are relative to *https://mecrm.dolylab.cc/api/v0.5*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pleades_kv_create**](KVApi.md#pleades_kv_create) | **GET** /kv | Create new Key-Value storage domain object.
[**pleades_kv_delete**](KVApi.md#pleades_kv_delete) | **DELETE** /kv/{hID}/field/{key} | DEL method (DELETE {key})
[**pleades_kv_get**](KVApi.md#pleades_kv_get) | **GET** /kv/{hID}/field/{key} | GET method of KV storage (GET {key})
[**pleades_kv_info**](KVApi.md#pleades_kv_info) | **GET** /kv/{hID} | Get KV-Storage object meta data
[**pleades_kv_set**](KVApi.md#pleades_kv_set) | **POST** /kv/{hID}/field/{key} | SET method of KV storage (SET {key} {body})
[**pleiades_kv_flush**](KVApi.md#pleiades_kv_flush) | **DELETE** /kv/{hID}/field | Remove all keys (FLUSH)
[**pleiades_kv_keys**](KVApi.md#pleiades_kv_keys) | **GET** /kv/{hID}/field | Get all keys (KEYS)

# **pleades_kv_create**
> pleades_kv_create()

Create new Key-Value storage domain object.

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()

try:
    # Create new Key-Value storage domain object.
    api_instance.pleades_kv_create()
except ApiException as e:
    print("Exception when calling KVApi->pleades_kv_create: %s\n" % e)
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

# **pleades_kv_delete**
> pleades_kv_delete(h_id, key)

DEL method (DELETE {key})

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()
h_id = 789 # int | KV Storage ID
key = 'key_example' # str | KV Storage Key

try:
    # DEL method (DELETE {key})
    api_instance.pleades_kv_delete(h_id, key)
except ApiException as e:
    print("Exception when calling KVApi->pleades_kv_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **h_id** | **int**| KV Storage ID | 
 **key** | **str**| KV Storage Key | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleades_kv_get**
> pleades_kv_get(h_id, key)

GET method of KV storage (GET {key})

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()
h_id = 789 # int | KV Storage ID
key = 'key_example' # str | KV Storage Key

try:
    # GET method of KV storage (GET {key})
    api_instance.pleades_kv_get(h_id, key)
except ApiException as e:
    print("Exception when calling KVApi->pleades_kv_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **h_id** | **int**| KV Storage ID | 
 **key** | **str**| KV Storage Key | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleades_kv_info**
> pleades_kv_info(h_id)

Get KV-Storage object meta data

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()
h_id = 789 # int | KV Storage ID

try:
    # Get KV-Storage object meta data
    api_instance.pleades_kv_info(h_id)
except ApiException as e:
    print("Exception when calling KVApi->pleades_kv_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **h_id** | **int**| KV Storage ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleades_kv_set**
> pleades_kv_set(h_id, key)

SET method of KV storage (SET {key} {body})

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()
h_id = 789 # int | KV Storage ID
key = 'key_example' # str | KV Storage Key

try:
    # SET method of KV storage (SET {key} {body})
    api_instance.pleades_kv_set(h_id, key)
except ApiException as e:
    print("Exception when calling KVApi->pleades_kv_set: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **h_id** | **int**| KV Storage ID | 
 **key** | **str**| KV Storage Key | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_kv_flush**
> pleiades_kv_flush(h_id)

Remove all keys (FLUSH)

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()
h_id = 789 # int | KV Storage ID

try:
    # Remove all keys (FLUSH)
    api_instance.pleiades_kv_flush(h_id)
except ApiException as e:
    print("Exception when calling KVApi->pleiades_kv_flush: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **h_id** | **int**| KV Storage ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_kv_keys**
> pleiades_kv_keys(h_id)

Get all keys (KEYS)

Not Implemented Yet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.KVApi()
h_id = 789 # int | KV Storage ID

try:
    # Get all keys (KEYS)
    api_instance.pleiades_kv_keys(h_id)
except ApiException as e:
    print("Exception when calling KVApi->pleiades_kv_keys: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **h_id** | **int**| KV Storage ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

