import httpx
import logging
from pydantic import Field

from .. import type


class Response(type.Response):
    code: int
    status: str
    worker_id: str = Field(alias="id")
    runtimes: list[str] = Field(alias="runtime")

    def from_response(response: httpx.Response) -> "Response":
        return Response(**response.json())


class Request(type.Request[Response]):
    runtimes: list[str] = Field(serialization_alias="runtime")

    def endpoint(self):
        return "/worker"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Registering worker: {self}")

        response = await client.post(
            self.endpoint(),
            json=self.model_dump(by_alias=True),
        )
        deserialized = Response.from_response(response)

        logging.debug(f"Registered worker: {deserialized}")
        return Response.from_response(response)
