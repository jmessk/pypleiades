import httpx
import logging
import io
from pydantic import Field

from .. import type


class Response(type.Response):
    code: int
    status: str
    data_id: str = Field(alias="id")
    checksum: str

    def from_response(response: httpx.Response) -> "Response":
        return Response(**response.json())


class Request(type.Request[Response]):
    data: bytes

    def endpoint(self):
        return "data"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Uploading data: {len(self.data)} bytes")

        blob = {"file": ("input", io.BytesIO(self.data))}
        response = await client.post(self.endpoint(), files=blob)
        deserialized = Response.from_response(response)

        logging.debug(f"Uploaded data: {deserialized}")
        return deserialized
