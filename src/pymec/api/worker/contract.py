import httpx
import logging
from typing import Optional
from pydantic import Field

from .. import type


class Response(type.Response):
    code: int
    status: str
    job_id: Optional[str] = Field(alias="job", default=None)

    def from_response(response: httpx.Response) -> "Response":
        return Response(**response.json())


class Request(type.Request[Response]):
    worker_id: str = Field(serialization_alias="id")
    tags: list[str] = Field(default=[])
    timeout: int

    def endpoint(self):
        return f"worker/{self.worker_id}/contract"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Creating contract: {self}")

        response = await client.post(
            self.endpoint(),
            json=self.model_dump(by_alias=True),
        )
        deserialized = Response.from_response(response)
        
        logging.debug(f"Created contract: {deserialized}")
        return deserialized
