from attrs import define, field
import logging
from result import Result, Ok, Err
from pydantic import BaseModel, Field
from typing import Optional

from . import MECAPI
from .api_types import Code


###############################################################


@define(slots=True, frozen=True)
class ReqWorkerRegist:
    """Register a worker
    method: `POST`
    endpoint: `/worker`

    type reqMsgWorkerRegist struct {
        Execulator []string `json:"runtime"`
    }
    """

    runtimes: list[str]

    def to_dict(self):
        return {"runtime": self.runtimes}


@define(slots=True, frozen=True)
class RespWorkerRegist:
    """Register a worker
    method: `POST`
    endpoint: `/worker`

    type respWorkerRegist struct {
        Code       int      `json:"code"`
        Status     string   `json:"status"`
        Message    string   `json:"message,omitempty"`
        WorkerId   int64    `json:"id,string,omitempty"`
        Execulator []string `json:"runtime,omitempty"`
    }
    """

    code: int
    status: str
    worker_id: str = field(alias="id")
    runtimes: list[str] = field(alias="runtime")


###############################################################


@define(slots=True, frozen=True)
class ReqWorkerContract:
    """Contract a worker
    method: `POST`
    endpoint: `/worker/{worker_id}/contract`

    type reqMsgWorkerContract struct {
        WorkerId int64    `json:"id,string,omitempty"`
        ExtraTag []string `json:"tags,omitempty"`
        MaxTimeo int      `json:"timeout,omitempty"`
    }
    """

    worker_id: str
    tags: list[str]
    timeout: int

    def to_dict(self):
        return {
            "id": self.worker_id,
            "tags": self.tags,
            "timeout": self.timeout,
        }


# @define(slots=True, frozen=True)
class RespWorkerContract(BaseModel):
    """Contract a worker
    method: `POST`
    endpoint: `/worker/{worker_id}/contract`

    type respMsgWorkerContract struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`
        JobId   *int64 `json:"job,string,omitempty"`
    }
    """

    code: int
    status: str
    job_id: Optional[str] = Field(alias="job", default=None)


###############################################################


@define(slots=True, frozen=True)
class RespWorkerInfo:
    """Get worker metadata
    method: `GET`
    endpoint: `/worker/{worker_id}`

    type respMsgWorkerInfo struct {
        Code       int      `json:"code"`
        Status     string   `json:"status"`
        Message    string   `json:"message,omitempty"`
        WorkerId   int64    `json:"id,string,omitempty"`
        Execulator []string `json:"runtime,omitempty"`
    }
    """

    code: int
    status: str
    worker_id: str = field(alias="id")
    runtimes: list[str] = field(alias="runtime")


###############################################################


class WorkerAPI(MECAPI):
    __slots__ = ["_server_url", "_logger", "_client", "_client_async"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(server_url, logger=logger, httpx_config=httpx_config)

    # register

    def register(self, runtimes: list[str]) -> Result[RespWorkerRegist, dict]:
        endpoint = f"{self._server_url}/worker"
        request_json = ReqWorkerRegist(runtimes=runtimes).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespWorkerRegist(**response_json))

    async def register_async(
        self,
        runtimes: list[str],
    ) -> Result[RespWorkerRegist, dict]:
        endpoint = f"{self._server_url}/worker"
        request_json = ReqWorkerRegist(runtimes=runtimes).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespWorkerRegist(**response_json))

    # contract

    def contract(
        self,
        worker_id: str,
        tags: list[str],
        timeout: int,
    ) -> Result[RespWorkerContract, dict]:
        endpoint = f"{self._server_url}/worker/{worker_id}/contract"

        request_json = ReqWorkerContract(
            worker_id=worker_id,
            tags=tags,
            timeout=timeout,
        ).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        match response_json.get("code"):
            case int(Code.OK):
                return Ok(RespWorkerContract(**response_json))
            case int(Code.NO_JOB):
                return Ok(RespWorkerContract(**response_json))
            case _:
                return Err(response_json)

    async def contract_async(
        self,
        worker_id: str,
        tags: list[str],
        timeout: int,
    ) -> Result[RespWorkerContract, dict]:
        endpoint = f"{self._server_url}/worker/{worker_id}/contract"

        request_json = ReqWorkerContract(
            worker_id=worker_id,
            tags=tags,
            timeout=timeout,
        ).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        match response_json.get("code"):
            case int(Code.OK):
                return Ok(RespWorkerContract(**response_json))
            case int(Code.NO_JOB):
                return Ok(RespWorkerContract(**response_json))
            case _:
                return Err(response_json)

    # info

    def info(self, worker_id: str) -> Result[RespWorkerInfo, dict]:
        endpoint = f"{self._server_url}/worker/{worker_id}"

        response = self._client.get(endpoint)

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespWorkerInfo(**response_json))

    async def info_async(
        self,
        worker_id: str,
    ) -> Result[RespWorkerInfo, dict]:
        endpoint = f"{self._server_url}/worker/{worker_id}"

        response = await self._client_async.get(endpoint)

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespWorkerInfo(**response_json))
