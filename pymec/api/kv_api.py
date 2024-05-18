from attrs import define, field
import logging
from result import Result, Ok, Err
from typing import Optional
from enum import Enum

from .pleiades_api import PleiadesAPI
from .api_types import Code


class KVConsistency(Enum):
    NONE = "none"
    EVENTUAL = "eventual"


@define(slots=True, frozen=True)
class ReqKVNamespaceCreate:
    consistency: KVConsistency

    def to_dict(self):
        return {
            "consistency": self.consistency.value,
        }


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
    namespace_id: str = field(alias="id")


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
    expire: int = field(default=0)
    get: bool = field(default=False)
    append: bool = field(default=False)

    def to_dict(self):
        return {
            "value": self.value,
            "expire": self.expire,
            "get": self.get,
            "append": self.append,
        }


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


class KVAPI(PleiadesAPI):
    __slots__ = ["_server_url", "_logger", "_client", "_client_async"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(server_url, logger=logger, httpx_config=httpx_config)

    # create namespace

    def create_namespace(
        self,
        consistency: KVConsistency = KVConsistency.NONE,
    ) -> Result[RespKVNamespaceCreate, dict]:
        endpoint = f"{self._server_url}/kv"

        request_json = ReqKVNamespaceCreate(
            consistency=consistency,
        ).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespKVNamespaceCreate(**response_json))

    async def create_namespace_async(
        self, consistency: Optional[KVConsistency]
    ) -> Result[RespKVNamespaceCreate, dict]:
        endpoint = f"{self._server_url}/kv"

        if consistency is None:
            request_json = ReqKVNamespaceCreate(
                consistency=KVConsistency.NONE,
            ).to_dict()
        else:
            request_json = ReqKVNamespaceCreate(
                consistency=consistency,
            ).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespKVNamespaceCreate(**response_json))

    # get value

    def get_value(self, namespace_id: str, key: str) -> Result[RespKVGet, dict]:
        endpoint = f"{self._server_url}/kv/{namespace_id}/field/{key}"

        response = self._client.get(endpoint)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespKVGet(**response_json))

    async def get_value_async(
        self,
        namespace_id: str,
        key: str,
    ) -> Result[RespKVGet, dict]:
        endpoint = f"{self._server_url}/kv/{namespace_id}/field/{key}"

        response = await self._client_async.get(endpoint)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespKVGet(**response_json))

    # set value

    def set_value(
        self,
        namespace_id: str,
        key: str,
        value: str,
        expire: int = 0,
        get: bool = False,
        append: bool = False,
    ) -> Result[RespKVSet, dict]:
        endpoint = f"{self._server_url}/kv/{namespace_id}/field/{key}"

        request_json = ReqKVSet(
            value=value,
            expire=expire,
            get=get,
            append=append,
        ).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespKVSet(**response_json))

    async def set_value_async(
        self,
        namespace_id: str,
        key: str,
        value: str,
        expire: int = 0,
        get: bool = False,
        append: bool = False,
    ) -> Result[RespKVSet, dict]:
        endpoint = f"{self._server_url}/kv/{namespace_id}/field/{key}"

        request_json = ReqKVSet(
            value=value,
            expire=expire,
            get=get,
            append=append,
        ).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespKVSet(**response_json))
