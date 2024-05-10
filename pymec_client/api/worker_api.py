from attrs import define, field
import httpx
import logging
from result import Result, Ok, Err

from api_types import Code


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
    message: str
    worker_id: str = field(alias="id")
    runtimes: list[str] = field(alias="runtime")


def register(server_url: str, runtimes: list[str]) -> Result[RespWorkerRegist, dict]:
    endpoint = f"{server_url}/worker"
    headers = {"Accept": "application/json"}

    request_json = ReqWorkerRegist(runtimes=runtimes).to_dict()

    with httpx.Client() as client:
        response = client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespWorkerRegist(**response_json))


async def register_async(
    server_url: str, runtimes: list[str]
) -> Result[RespWorkerRegist, dict]:
    endpoint = f"{server_url}/worker"
    headers = {"Accept": "application/json"}

    request_json = ReqWorkerRegist(runtimes=runtimes).to_dict()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespWorkerRegist(**response_json))


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


@define(slots=True, frozen=True)
class RespWorkerContract:
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
    message: str
    job_id: str = field(alias="id")


def contract(
    server_url: str,
    worker_id: str,
    tags: list[str],
    timeout: int,
) -> Result[RespWorkerContract, dict]:
    endpoint = f"{server_url}/worker/{worker_id}/contract"
    headers = {"Accept": "application/json"}

    request_json = ReqWorkerContract(
        worker_id=worker_id,
        tags=tags,
        timeout=timeout,
    ).to_dict()

    with httpx.Client() as client:
        response = client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespWorkerContract(**response_json))


async def contract_async(
    server_url: str,
    worker_id: str,
    tags: list[str],
    timeout: int,
) -> Result[RespWorkerContract, dict]:
    endpoint = f"{server_url}/worker/{worker_id}/contract"
    headers = {"Accept": "application/json"}

    request_json = ReqWorkerContract(
        worker_id=worker_id,
        tags=tags,
        timeout=timeout,
    ).to_dict()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespWorkerContract(**response_json))


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
    message: str
    worker_id: str = field(alias="id")
    runtimes: list[str] = field(alias="runtime")


def info(server_url: str, worker_id: str) -> Result[RespWorkerInfo, dict]:
    endpoint = f"{server_url}/worker/{worker_id}"
    headers = {"Accept": "application/json"}

    with httpx.Client() as client:
        response = client.get(
            endpoint,
            headers=headers,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespWorkerInfo(**response_json))


async def info_async(
    server_url: str,
    worker_id: str,
) -> Result[RespWorkerInfo, dict]:
    endpoint = f"{server_url}/worker/{worker_id}"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            endpoint,
            headers=headers,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespWorkerInfo(**response_json))
