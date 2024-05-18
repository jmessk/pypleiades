from attrs import define, field
import logging
from result import Result, Ok, Err
from typing import Optional

from .pleiades_api import PleiadesAPI
from .api_types import Code


###############################################################


@define(slots=True, frozen=True)
class ReqLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`

    type reqMsgFunctioCreate struct {
        CodeId int64  `json:"codex,string"`
        Runt   string `json:"runtime,omitempty"`
    }
    """

    data_id: str
    runtime: str

    def to_dict(self):
        return {
            "codex": self.data_id,
            "runtime": self.runtime,
        }


@define(slots=True, frozen=True)
class RespLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`

    type respMsgFunctioCreate struct {
        Code   int    `json:"code"`
        Status string `json:"status"`
        Id     int64  `json:"id,string"`
    }
    """

    code: int
    status: str
    lambda_id: str = field(alias="id")


###############################################################


@define(slots=True, frozen=True)
class RespLambdaInfo:
    """Get lambda metadata
    method: `GET`
    endpoint: `/lambda/{lambda_id}`

    type respMsgFunctioRead struct {
        Code      int    `json:"code"`
        Status    string `json:"status"`
        Message   string `json:"message,omitempty"`
        FunctioId int64  `json:"id,string,omitempty"`
        CodeId    int64  `json:"codex,string,omitempty"`
        Runt      string `json:"runtime,omitempty"`
    }
    """

    code: int
    status: str
    lambda_id: str = field(alias="id")
    data_id: str = field(alias="codex")
    runtime: str


###############################################################


class LambdaAPI(PleiadesAPI):
    __slots__ = ["_server_url", "_logger", "_client", "_client_async"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(server_url, logger=logger, httpx_config=httpx_config)

    # create

    def create(self, data_id: str, runtime: str) -> Result[RespLambdaCreate, dict]:
        endpoint = f"{self._server_url}/lambda"

        request_json = ReqLambdaCreate(
            data_id=data_id,
            runtime=runtime,
        ).to_dict()

        response = self._client.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespLambdaCreate(**response_json))

    async def create_async(
        self,
        data_id: str,
        runtime: str,
    ) -> Result[RespLambdaCreate, dict]:
        endpoint = f"{self._server_url}/lambda"

        request_json = ReqLambdaCreate(
            data_id=data_id,
            runtime=runtime,
        ).to_dict()

        response = await self._client_async.post(endpoint, json=request_json)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespLambdaCreate(**response_json))

    # info

    def info(self, lambda_id: str) -> Result[RespLambdaInfo, dict]:
        endpoint = f"{self._server_url}/lambda/{lambda_id}"

        response = self._client.get(endpoint)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespLambdaInfo(**response_json))

    async def info_async(self, lambda_id: str) -> Result[RespLambdaInfo, dict]:
        endpoint = f"{self._server_url}/lambda/{lambda_id}"

        response = await self._client_async.get(endpoint)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespLambdaInfo(**response_json))
