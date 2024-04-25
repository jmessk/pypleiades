# ResponseFunctionInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] 
**status** | **str** |  | [optional] 
**fid** | **str** | Function ID. This ID should be an 64-bit signed integer. since JSON is not able to handle 64-bit unsigned integer, use string instead. | [optional] 
**code_id** | **str** | Code ID.  This ID will be a valid BLOB data object ID which can be download by &#x60;GET /data/{this ID}/blob&#x60;  This ID should be an 64-bit signed integer reference to an existing blob data since JSON is not able to handle 64-bit unsigned integer, use string instead. | [optional] 
**runtime** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

