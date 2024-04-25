# RequestFunctionCreate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code_id** | **str** | Codex ID.  Hic campus debet esse validus ID adhibet ad obiectum BLOB datum (alias, dID). (Verificatio validitatis nondum implementata est)  Non suadetur: Si haec functio anonyma nullam postulationem scripti requirit, uti potes 0 ut valor huius campi. In hoc systemate, 0 erit validus BLOB objectus ID qui normaliter per GET /data/0/blob potest descendi. (Nondum implementatum)  Hic ID debet esse integer signatus 64-bitum adhibet ad praesens obiectum BLOB datum, quia JSON non potest integer non signatum 64-bitum tractare, stringam utere. | 
**runtime** | **str** | The runtime field corresponds to the interpreter that should be used by this anonymous function. Currently, the system does not perform any validity checks on this field, and using a runtime name that does not exist in the system will generate a new corresponding runtime. This runtime field will be used for capability checks, so it needs to match the field used for logging in the worker.  Campus &#x60;runtime&#x60; ad interpretatorem respondet, qui ab hac functione anonyma uti debet. Hactenus, systema nullas probationes de validitate in hoc campo agit, et nomen campus runtime, quod in systemate non existit, generabit novum campus runtime correspondens. Hic campus &#x60;runtime&#x60; ad probationes facultatis utetur, itaque congruere debet cum campo, qui ad logginum in opifice utitur. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

