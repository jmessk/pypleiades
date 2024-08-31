from .. import api
import httpx
from pydantic import Field


class Response(api.Response):
    code: int
    status: str
    message: str

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    job_id: str = Field(exclude=True)
    data_id: str = Field(serialization_alias="output")
    status: str = Field(serialization_alias="status")

    def endpoint(self):
        return f"job/{self.job_id}"

    async def send(self, client: httpx.AsyncClient) -> Response:
        response = await client.post(self.endpoint(), json=self.model_dump(by_alias=True))

        return Response.from_response(response)
