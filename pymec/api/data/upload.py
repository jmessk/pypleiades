from .. import api
import httpx
import io
from pydantic import Field


class Response(api.Response):
    code: int
    status: str
    data_id: str = Field(alias="id")
    checksum: str

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    data: bytes

    def endpoint(self):
        return "data"

    async def send(self, client: httpx.AsyncClient) -> Response:
        blob = {"file": ("input", io.BytesIO(self.data))}
        response = await client.post(self.endpoint(), files=blob)

        return Response.from_response(response)
