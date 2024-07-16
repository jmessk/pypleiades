from ..api_types import Request, Response
import httpx
from typing import override
from urllib.parse import urljoin
from pydantic import Field


class WorkerRegisterResponse(Response):
    code: int
    status: str
    worker_id: str = Field(alias="id")

    @override
    def from_response(response: httpx.Response):
        return WorkerRegisterResponse(**response.json())


class WorkerRegisterRequest(Request[WorkerRegisterResponse]):
    runtimes: list[str] = Field(serialization_alias="runtime")

    @override
    def endpoint(self):
        return "worker"

    @override
    async def send(
        self,
        client: httpx.AsyncClient,
        host: str,
    ) -> WorkerRegisterResponse:
        url = urljoin(host, self.endpoint())
        response = await client.post(url, json=self.model_dump(by_alias=True))
        return WorkerRegisterResponse.from_response(response)
