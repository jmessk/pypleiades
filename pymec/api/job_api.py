from attrs import define, field
import httpx
import logging
from result import Result, Ok, Err
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from . import MECAPI
from .api_types import Code


###############################################################


@define(slots=True, frozen=True)
class ReqJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`

    type reqMsgJobCreate struct {
        InputDataId int64    `json:"input,string"`
        FunctionId  int64    `json:"lambda,string"`
        ExtraTag    []string `json:"tags"`
    }
    """

    data_id: str
    lambda_id: str
    tags: list[str]

    def to_dict(self):
        return {
            "input": self.data_id,
            "lambda": self.lambda_id,
            "tags": self.tags,
        }


@define(slots=True, frozen=True)
class RespJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`

    type respMsgJobCreate struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`
        JobId   int64  `json:"id,string,omitempty"`
    }
    """

    code: int
    status: str
    job_id: str = field(alias="id")


###############################################################


class Lambda(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    lambda_id: str = Field(alias="id")
    runtime: str
    data_id: str = Field(alias="codex")


class InputData(BaseModel):
    data_id: str = Field(alias="id")


class OutputData(BaseModel):
    data_id: str = Field(alias="id")


class RespJobInfo(BaseModel):
    code: int
    status: str
    job_id: str = Field(alias="id")
    job_status: str = Field(alias="state")
    lambda_: Lambda = Field(alias="lambda")
    input: InputData
    output: Optional[OutputData] = Field(default=None)
    # tags: list[str]


###############################################################


@define(slots=True, frozen=True)
class ReqJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`

    type reqMsgJobUpdate struct {
        id     int64
        Output *int64  `json:"output,string,omitempty"`
        Status *string `json:"status,omitempty"`
        State  *string `json:"state,omitempty"`
    }
    """

    data_id: str
    status: str
    job_status: str

    def to_dict(self):
        return {
            "output": self.data_id,
            "status": self.status,
            "state": self.job_status,
        }


@define(slots=True, frozen=True)
class RespJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`

    type respMsgJobUpdate struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`
    }
    """

    code: int
    status: str
    message: str


###############################################################


class JobAPI(MECAPI):
    __slots__ = ["_server_url", "_logger", "_client", "_client_async"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(server_url, logger=logger, httpx_config=httpx_config)

    # create

    def create(
        self,
        lambda_id: str,
        data_id: str,
        tags: list[str],
    ) -> Result[RespJobCreate, dict]:
        endpoint = f"{self._server_url}/job"

        request_json = ReqJobCreate(
            data_id=data_id,
            lambda_id=lambda_id,
            tags=tags,
        ).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespJobCreate(**response_json))

    async def create_async(
        self,
        lambda_id: str,
        data_id: str,
        tags: list[str],
    ) -> Result[RespJobCreate, dict]:
        endpoint = f"{self._server_url}/job"

        request_json = ReqJobCreate(
            data_id=data_id,
            lambda_id=lambda_id,
            tags=tags,
        ).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespJobCreate(**response_json))

    # info

    def info(
        self,
        job_id: str,
        except_status: Optional[str] = None,
        timeout_s: int = 0,
    ) -> Result[RespJobInfo, dict]:
        endpoint = f"{self._server_url}/job/{job_id}"

        if timeout_s == 0:
            response = self._client.get(endpoint)

        else:
            response = self._client.get(
                endpoint,
                params={
                    "except": except_status,
                    "timeout": timeout_s,
                },
            )

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespJobInfo(**response_json))

    async def info_async(
        self,
        job_id: str,
        except_status: Optional[str] = None,
        timeout_s: int = 0,
    ) -> Result[RespJobInfo, dict]:
        endpoint = f"{self._server_url}/job/{job_id}"

        if timeout_s == 0:
            response = await self._client_async.get(endpoint)
        else:
            response = await self._client_async.get(
                endpoint,
                params={
                    "except": except_status,
                    "timeout": timeout_s,
                },
            )

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespJobInfo(**response_json))

    # update

    def update(
        self,
        job_id: str,
        output_data_id: str,
        status: str,
    ) -> Result[RespJobUpdate, dict]:
        endpoint = f"{self._server_url}/job/{job_id}"

        request_json = ReqJobUpdate(
            data_id=output_data_id,
            status=status,
            job_status=status,
        ).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespJobUpdate(**response_json))

    async def update_async(
        self,
        job_id: str,
        output_data_id: str,
        status: str,
    ) -> Result[RespJobUpdate, dict]:
        endpoint = f"{self._server_url}/job/{job_id}"

        request_json = ReqJobUpdate(
            data_id=output_data_id,
            status=status,
            job_status=status,
        ).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != int(Code.OK):
            return Err(response_json)

        return Ok(RespJobUpdate(**response_json))
