from .. import api
import httpx
from pydantic import Field


class Response(api.Response):
    code: int
    status: str
    job_id: str = Field(alias="id")

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    lambda_id: str = Field(serialization_alias="lambda")
    data_id: str = Field(serialization_alias="input")
    tags: list[str]

    def endpoint(self):
        return "job"

    async def send(self, client: httpx.AsyncClient) -> Response:
        response = await client.post(self.endpoint(), json=self.model_dump(by_alias=True))

        return Response.from_response(response)
