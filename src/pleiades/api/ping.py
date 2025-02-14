import httpx
import logging
from pydantic import Field

from . import type


class Response(type.Response):
    code: int
    status: str
    message: str

    def from_response(response: httpx.Response) -> "Response":
        return Response(**response.json())


class Request(type.Request[Response]):
    def endpoint(self):
        return "ping"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Sending a ping: {self}")

        response = await client.get(self.endpoint())
        deserialized = Response.from_response(response)

        logging.debug(f"Reacieve a ping: {deserialized}")
        return deserialized
