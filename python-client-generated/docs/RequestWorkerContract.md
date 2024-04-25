# RequestWorkerContract

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**extra_tag** | **list[str]** | Extra tag list (only for this request). | [optional] 
**worker_id** | **str** | Worker ID. This ID should be an 64-bit signed integer. since JSON is not able to handle 64-bit unsigned integer, use string instead. | [optional] 
**timeout** | **int** | Maximum timeout in seconds. This value should be an 32-bit signed integer. Note that the RM will return the result before the timeout even if no job is available. The real timeout will be less then the minimum of this value and the RM side global timeout. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

