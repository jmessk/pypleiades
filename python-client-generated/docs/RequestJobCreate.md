# RequestJobCreate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input_id** | **str** | Input data ID.  This ID should be a valid BLOB data object ID (aka, &#x60;dID&#x60;)  This ID should be an 64-bit signed integer. Since JSON is not able to handle 64-bit unsigned integer, use string instead. | [optional] 
**functio** | **str** | Function ID.  This ID should be a valid lambda functione object ID (aka, &#x60;fID&#x60;) This ID should be an 64-bit signed integer. since JSON is not able to handle 64-bit unsigned integer, use string instead. | [optional] 
**extra_tag** | **list[str]** | Extra tag list.  The tag that the lambda function object hold will automatically applied to the Job object. This field is used to append extra tags that not given by function object.  This object should be an array of strings.  Tags are defaultly treated as suggested tag, which means the more tags matched, the higher score the worker will be given. The suggested tag will only be used to calculate the worker score, the system will not insure that all tags are matched.  (Not Implemented Yet) Put a &#x60;+&#x60; character at the begining of the tag will transfer it into a Necessary tag. which will be treated as same as what runtime do.  (Not Implemented Yet) Put a &#x60;-&#x60; character at the begining of the tag string will transfer it into a Reject tag. If worker contains any of the reject tags, the worker will not be matched. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

