from .. import api
import httpx
from typing import Optional
from pydantic import Field, BaseModel


class Lambda(BaseModel):
    lambda_id: str = Field(alias="id")
    runtime: str
    data_id: str = Field(alias="codex")


class Input(BaseModel):
    data_id: str = Field(alias="id")


class Output(BaseModel):
    data_id: str = Field(alias="id")


class Response(api.Response):
    code: int
    status: str
    job_id: str = Field(alias="id")
    job_status: str = Field(alias="state")
    lambda_: Lambda = Field(alias="lambda")
    input: Input
    output: Optional[Output] = Field(default=None)

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    job_id: str
    except_: Optional[str] = Field(serialization_alias="except", default=None)
    timeout: Optional[int] = Field(default=None)

    def endpoint(self):
        return f"job/{self.job_id}"

    async def send(self, client: httpx.AsyncClient) -> Response:
        if self.except_ is None:
            params = {}
        else:
            params = {"except": self.except_, "timeout": self.timeout}

        response = await client.get(self.endpoint(), params=params)

        return Response.from_response(response)
