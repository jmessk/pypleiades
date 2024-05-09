from attrs import define, field
import httpx
import logging
from result import Result, Ok, Err

from api_types import Code


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


def create_lambda(
    server_url, data_id: str, runtime: str
) -> Result[RespLambdaCreate, dict]:
    endpoint = f"{server_url}/lambda"
    headers = {"Accept": "application/json"}

    request_json = ReqLambdaCreate(
        data_id=data_id,
        runtime=runtime,
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

    return Ok(RespLambdaCreate(**response_json))


async def create_lambda_async(
    server_url, data_id: str, runtime: str
) -> Result[RespLambdaCreate, dict]:
    endpoint = f"{server_url}/lambda"
    headers = {"Accept": "application/json"}

    request_json = ReqLambdaCreate(
        data_id=data_id,
        runtime=runtime,
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

    return Ok(RespLambdaCreate(**response_json))


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
    message: str
    lambda_id: str = field(alias="id")
    data_id: str = field(alias="codex")
    runtime: str


def get_lambda_info(server_url, lambda_id: str) -> Result[RespLambdaInfo, dict]:
    endpoint = f"{server_url}/lambda/{lambda_id}"
    headers = {"Accept": "application/json"}

    with httpx.Client() as client:
        response = client.get(
            endpoint,
            headers=headers,
        )

    response_json = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespLambdaInfo(**response_json))


async def get_lambda_info_async(
    server_url, lambda_id: str
) -> Result[RespLambdaInfo, dict]:
    endpoint = f"{server_url}/lambda/{lambda_id}"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            endpoint,
            headers=headers,
        )

    response_json = response.json()
    logging.debug(response_json)

    if response_json.get("code") != Code.OK:
        return Err(response_json)

    return Ok(RespLambdaInfo(**response_json))
