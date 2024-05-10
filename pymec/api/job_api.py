from attrs import define, field
import httpx
import logging
from result import Result, Ok, Err

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
    message: str
    job_id: str = field(alias="id")


def create_job(
    server_url: str,
    lambda_id: str,
    data_id: str,
    tags: list[str],
) -> Result[RespJobCreate, dict]:
    endpoint = f"{server_url}/job"
    headers = {"Accept": "application/json"}

    request_json = ReqJobCreate(
        data_id=data_id,
        lambda_id=lambda_id,
        tags=tags,
    ).to_dict()

    with httpx.Client() as client:
        response = client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != int(Code.OK):
        return Err(response_json)

    return Ok(RespJobCreate(**response_json))


async def create_job_async(
    server_url: str,
    lambda_id: str,
    data_id: str,
    tags: list[str],
) -> Result[RespJobCreate, dict]:
    endpoint = f"{server_url}/job"
    headers = {"Accept": "application/json"}

    request_json = ReqJobCreate(
        data_id=data_id,
        lambda_id=lambda_id,
        tags=tags,
    ).to_dict()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != int(Code.OK):
        return Err(response_json)

    return Ok(RespJobCreate(**response_json))


###############################################################


@define(slots=True, frozen=True)
class Lambda:
    """
    type respJobLambda struct {
        Id      int64  `json:"id,string"`
        Runtime string `json:"runtime"`
        Code    int    `json:"codex"`
    }
    """

    lambda_id: str = field(alias="id")
    runtime: str
    data_id: str = field(alias="codex")


@define(slots=True, frozen=True)
class RespJobInfo:
    """Get job metadata
    method: `GET`
    endpoint: `/job/{job_id}`

    type respMsgJobInfo struct {
        Code              int    `json:"code"`
        Status            string `json:"status"`
        Message           string `json:"message,omitempty"`
        JobId             int64  `json:"id,string,omitempty"`
        JobStatus         string `json:"job_status,omitempty"`
        JobInputData      *int64 `json:"job_input_id,string"`
        JobOutputData     *int64 `json:"job_output_id,string"`
        JobFunctio        int64  `json:"functio,string,omitempty"`
        JobFunctioRuntime string `json:"runtime,omitempty"`
        // New Format
        Tags   []string      `json:"tags,omitempty"`
        Lambda respJobLambda `json:"lambda"`
        Input  *respJobData  `json:"input,omitempty"`
        Output *respJobData  `json:"output,omitempty"`
        State  string        `json:"state,omitempty"`
    }
    """

    code: int
    status: str
    job_id: str = field(alias="id")
    job_status: str
    input_data_id: str = field(alias="job_input_id")
    output_data_id: str = field(alias="job_output_id")
    lambda_id: str = field(alias="functio")
    lambda_: Lambda = field(alias="lambda")
    state: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            code=data["code"],
            status=data["status"],
            job_id=data["id"],
            job_status=data["job_status"],
            input_data_id=data["job_input_id"],
            output_data_id=data["job_output_id"],
            lambda_id=data["functio"],
            lambda_=Lambda(**data["lambda"]),
            state=data["state"],
        )


def info(server_url: str, job_id: str) -> Result[RespJobInfo, dict]:
    endpoint = f"{server_url}/job/{job_id}"
    headers = {"Accept": "application/json"}

    with httpx.Client() as client:
        response = client.get(
            endpoint,
            headers=headers,
        )

    response_json = response.json()
    logging.debug(response_json)

    if response_json.get("code") != int(Code.OK):
        return Err(response_json)

    return Ok(RespJobInfo.from_dict(response_json))


async def info_async(server_url: str, job_id: str) -> Result[RespJobInfo, dict]:
    endpoint = f"{server_url}/job/{job_id}"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            endpoint,
            headers=headers,
        )

    response_json = response.json()
    logging.debug(response_json)

    if response_json.get("code") != int(Code.OK):
        return Err(response_json)

    return Ok(RespJobInfo.from_dict(response_json))


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

    output_data_id: str
    status: str
    job_status: str

    def to_dict(self):
        return {
            "output": self.output_data_id,
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


def update_status(
    server_url: str,
    job_id: str,
    output_data_id: str,
    status: str,
) -> Result[RespJobUpdate, dict]:
    endpoint = f"{server_url}/job/{job_id}"
    headers = {"Accept": "application/json"}

    request_json = ReqJobUpdate(
        output_data_id=output_data_id,
        status=status,
        job_status=status,
    ).to_dict()

    with httpx.Client() as client:
        response = client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != int(Code.OK):
        return Err(response_json)

    return Ok(RespJobUpdate(**response_json))


async def update_status_async(
    server_url: str,
    job_id: str,
    output_data_id: str,
    status: str,
) -> Result[RespJobUpdate, dict]:
    endpoint = f"{server_url}/job/{job_id}"
    headers = {"Accept": "application/json"}

    request_json = ReqJobUpdate(
        output_data_id=output_data_id,
        status=status,
        job_status=status,
    ).to_dict()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=request_json,
        )

    response_json: dict[str, str] = response.json()
    logging.debug(response_json)

    if response_json.get("code") != int(Code.OK):
        return Err(response_json)

    return Ok(RespJobUpdate(**response_json))
