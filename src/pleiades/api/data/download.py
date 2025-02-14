import httpx
import logging

from .. import type


class Response(type.Response):
    data: bytes

    def from_response(response: httpx.Response) -> "Response":
        return Response(data=response.content)


class Request(type.Request[Response]):
    data_id: str

    def endpoint(self):
        return f"/data/{self.data_id}/blob"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Downloading data: {self}")

        response = await client.get(self.endpoint())
        deserialized = Response.from_response(response)

        logging.debug(f"Downloaded data: {len(deserialized.data)} bytes")
        return deserialized
