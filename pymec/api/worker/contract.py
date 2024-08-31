from .. import api
import httpx
from typing import Optional
from pydantic import Field


class Response(api.Response):
    code: int
    status: str
    job_id: Optional[str] = Field(alias="job", default=None)

    def from_response(response: httpx.Response):
        return Response(**response.json())


class Request(api.Request[Response]):
    worker_id: str = Field(serialization_alias="id")
    tags: list[str]
    timeout: int

    def endpoint(self):
        return f"worker/{self.worker_id}/contract"

    async def send(self, client: httpx.AsyncClient) -> Response:
        response = await client.post(
            self.endpoint(),
            json=self.model_dump(by_alias=True),
        )

        return Response.from_response(response)
