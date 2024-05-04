from attrs import define, field
import httpx
import logging


@define(slots=True, frozen=True)
class ReqKVNamespaceCreate:
    pass


@define(slots=True, frozen=True)
class RespKVNamespaceCreate:
    """
    type respMsgKVCreate struct {
        Code   int    `json:"code"`
        Status string `json:"status"`
        Id     int64  `json:"id,string"`
    }
    """

    code: int
    status: str
    namespace: str = field(alias="id")


###############################################################


@define(slots=True, frozen=True)
class ReqKVNamespaceInfo:
    """
    type reqMsgKVInfo struct {
        NameSpace int64 `json:"id,string"`
    }
    """

    pass


@define(slots=True, frozen=True)
class RespKVNamespaceInfo:
    """
    type respMsgKVInfo struct {
        Code   int    `json:"code"`
        Status string `json:"status"`
        KVId   int64  `json:"id,string,omitempty"`
    }
    """

    code: int
    status: str
    kv_id: str = field(alias="id")


###############################################################


@define(slots=True, frozen=True)
class RespKVGet:
    """
    type respMsgKVGet struct {
        Code   int    `json:"code"`
        Status string `json:"status"`
        Value  string `json:"value,omitempty"`
    }
    """

    code: int
    status: str
    value: str


###############################################################


@define(slots=True, frozen=True)
class ReqKVSet:
    """
    type reqMsgKVSet struct {
        nameSpace int64  `param:"nID"`
        key       string `param:"key"`
        Value     string `json:"value"`
    }
    """

    value: str


@define(slots=True, frozen=True)
class RespKVSet:
    """
    type respMsgKVSet struct {
        Code   int    `json:"code"`
        Status string `json:"status"`
        Value  string `json:"value,omitempty"`
    }
    """

    code: int
    status: str
    value: str
