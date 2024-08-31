from .. import api
import httpx
from pydantic import Field


class Response(api.Response):
    code: int
    status: str
    worker_id: str = Field(alias="id")

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    runtimes: list[str] = Field(serialization_alias="runtime")

    def endpoint(self):
        return "worker"

    async def send(self, client: httpx.AsyncClient) -> Response:
        response = await client.post(
            self.endpoint(),
            json=self.model_dump(by_alias=True),
        )
        return Response.from_response(response)
