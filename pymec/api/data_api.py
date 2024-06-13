from attrs import define, field
import logging
import io
from result import Result, Ok, Err
from typing import Optional

from .pleiades_api import PleiadesAPI
from .api_types import Code


###############################################################


@define(slots=True, frozen=True)
class RespDataCreate:
    """Create a BLOB
    method: `POST`
    endpoint: `/data`

    type respMessageDataCreate struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`

        DataID   int64  `json:"id,string"`
        DataHash string `json:"checksum"`
    }
    """

    code: int
    status: str
    data_id: str = field(alias="id")
    checksum: str


###############################################################


@define(slots=True, frozen=True)
class RespDataInfo:
    """Get BLOB metadata
    method: `GET`
    endpoint: `/data/{data_id}`

    type respMsgDataRead struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`

        DataID   int64  `json:"id,string,omitempty"`
        DataHash string `json:"checksum,omitempty"`
    }
    """

    code: int
    status: str
    data_id: str = field(alias="id")
    checksum: str


###############################################################


class DataAPI(PleiadesAPI):
    __slots__ = ["_server_url", "_logger", "_client", "_client_async"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(server_url, logger=logger, httpx_config=httpx_config)

    # get data

    def get_data(self, data_id: str) -> Result[bytes, dict]:
        endpoint = f"{self._server_url}/data/{data_id}/blob"

        response = self._client.get(endpoint)

        # If the response is JSON, return the JSON object
        # `response.headers` returns a `CaseInsensitiveDict`
        if response.headers.get("content-type") == "application/json":
            response_json: dict = response.json()
            self._logger.debug(response_json)

            return Err(response_json)

        self._logger.debug("content-type: application/octet-stream")

        return Ok(response.content)

    async def get_data_async(self, data_id: str) -> Result[bytes, dict]:
        endpoint = f"{self._server_url}/data/{data_id}/blob"

        response = await self._client_async.get(endpoint)

        # If the response is JSON, return the JSON object
        # `response.headers` returns a `CaseInsensitiveDict`
        if response.headers.get("content-type") == "application/json":
            response_json: dict = response.json()
            self._logger.debug(response_json)

            return Err(response_json)

        self._logger.debug("content-type: application/octet-stream")

        return Ok(response.content)

    # post data

    def post_data(
        self,
        data_bytes: bytes,
    ) -> Result[RespDataCreate, dict]:
        endpoint = f"{self._server_url}/data"

        file = {"file": ("input", io.BytesIO(data_bytes))}

        import time
        start = time.perf_counter()
        response = self._client.post(endpoint, files=file)
        end = time.perf_counter()
        print(f"post_data: {end - start}")

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespDataCreate(**response_json))

    async def post_data_async(
        self,
        data_bytes: bytes,
    ) -> Result[RespDataCreate, dict]:
        endpoint = f"{self._server_url}/data"

        file = {"file": ("input", io.BytesIO(data_bytes))}

        response = await self._client_async.post(endpoint, files=file)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespDataCreate(**response_json))

    # info

    def info(self, data_id: str) -> Result[RespDataInfo, dict]:
        endpoint = f"{self._server_url}/data/{data_id}"

        response = self._client.get(endpoint)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespDataInfo(**response_json))

    async def info_async(self, data_id: str) -> Result[RespDataInfo, dict]:
        endpoint = f"{self._server_url}/data/{data_id}"

        response = await self._client_async.get(endpoint)

        response_json: dict = response.json()
        self._logger.debug(response_json)

        if response_json.get("code") != Code.OK.value:
            return Err(response_json)

        return Ok(RespDataInfo(**response_json))
