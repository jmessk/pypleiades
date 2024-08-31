from .. import api
import httpx
from pydantic import Field


class Response(api.Response):
    code: int
    status: str
    lambda_id: str = Field(alias="id")

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    data_id: str = Field(serialization_alias="codex")
    runtime: str

    def endpoint(self):
        return "lambda"

    async def send(self, client: httpx.AsyncClient) -> Response:
        response = await client.post(self.endpoint(), json=self.model_dump(by_alias=True))

        return Response.from_response(response)
