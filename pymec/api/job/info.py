from ..api_types import Request, Response
import httpx
from typing import Optional
from urllib.parse import urljoin
from pydantic import Field, BaseModel


class Lambda(BaseModel):
    lambda_id: str = Field(alias="id")
    runtime: str
    data_id: str = Field(alias="codex")


class Input(BaseModel):
    data_id: str = Field(alias="id")


class Output(BaseModel):
    data_id: str = Field(alias="id")


class JobInfoResponse(Response):
    code: int
    status: str
    job_id: str = Field(alias="id")
    job_status: str = Field(alias="state")
    lambda_: Lambda = Field(alias="lambda")
    input: Input
    output: Optional[Output] = Field(default=None)

    def from_response(response: httpx.Response):
        return JobInfoResponse(**response.json())


class JobInfoRequest(Request[JobInfoResponse]):
    job_id: str
    except_: Optional[str] = Field(serialization_alias="except", default=None)
    timeout: Optional[int] = Field(default=None)

    def endpoint(self):
        return f"job/{self.job_id}"

    async def send(self, client: httpx.AsyncClient, host: str) -> JobInfoResponse:
        if self.except_ is None:
            params = {}
        else:
            params = {"except": self.except_, "timeout": self.timeout}

        url = urljoin(host, self.endpoint())
        response = await client.get(url, params=params)

        return JobInfoResponse.from_response(response)
