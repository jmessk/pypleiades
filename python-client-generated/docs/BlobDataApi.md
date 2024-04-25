# swagger_client.BlobDataApi

All URIs are relative to *https://mecrm.dolylab.cc/api/v0.5*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pleiades_data_download**](BlobDataApi.md#pleiades_data_download) | **GET** /data/{dID}/blob | Download BLOD data
[**pleiades_data_meta**](BlobDataApi.md#pleiades_data_meta) | **GET** /data/{dID} | Get meta data of a BLOB data object
[**pleiades_data_upload**](BlobDataApi.md#pleiades_data_upload) | **POST** /data | Upload BLOB data

# **pleiades_data_download**
> str pleiades_data_download(d_id)

Download BLOD data

Download blob data

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BlobDataApi()
d_id = 'd_id_example' # str | Data ID. This ID should be a valid BLOB data object ID.

try:
    # Download BLOD data
    api_response = api_instance.pleiades_data_download(d_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlobDataApi->pleiades_data_download: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **d_id** | **str**| Data ID. This ID should be a valid BLOB data object ID. | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_data_meta**
> ResponseDataMeta pleiades_data_meta(d_id)

Get meta data of a BLOB data object

Get meta data of a BLOB data object.  This endpoint can be used to check if a BLOB data object is exist.  The return values of this API may contain fields that have not been mentioned in the documentation. These fields could be experimental or deprecated fields that are subject to change. Developers should ignore the presence of these fields.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BlobDataApi()
d_id = 'd_id_example' # str | Data ID. This ID should be a valid BLOB data object ID.

try:
    # Get meta data of a BLOB data object
    api_response = api_instance.pleiades_data_meta(d_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlobDataApi->pleiades_data_meta: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **d_id** | **str**| Data ID. This ID should be a valid BLOB data object ID. | 

### Return type

[**ResponseDataMeta**](ResponseDataMeta.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pleiades_data_upload**
> ResponseDataUpload pleiades_data_upload(file=file)

Upload BLOB data

Use this endpoint to upload new BLOB (Binary Large OBject)  This endpoint will give the uploaded BLOB object an globally unique identifier. Currently this globally unique identifier is a 64-bit signed integer, which exhibits a non-strictly monotonic increasing trend over time.  The identifier given by this endpoint will be called `dID` in this system which stands for \"blob **d**ata object **ID**\"  The BLOB data object has 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BlobDataApi()
file = 'file_example' # str |  (optional)

try:
    # Upload BLOB data
    api_response = api_instance.pleiades_data_upload(file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlobDataApi->pleiades_data_upload: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **str**|  | [optional] 

### Return type

[**ResponseDataUpload**](ResponseDataUpload.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

