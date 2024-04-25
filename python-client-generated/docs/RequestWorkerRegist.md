# RequestWorkerRegist

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**runtimes** | **list[str]** | Runtime (interperter) list.  If no runtime given, the &#x60;default&#x60; runtime will be assigned to the worker, which should not be used by any job.  We suggest using the format of &#x60;Base[+Feature]&#x60; format here. For example, now we have a interperter called &#x60;dlabLua54&#x60;, we can append a new feature plugin to this interperter called &#x60;pcli&#x60;(pleiades client), so we should also create a runtime called &#x60;dlabLua54+pcli&#x60;  Currently our scheduler will not consider about the feature plugin, so we need to write all possible runtimes here.  Also, you can regist an non-interperter runtime, which using no lambda function as script input. See Also: &#x60;POST /lambda&#x60; | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

