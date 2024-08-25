from ..api_types import Request, Response
import httpx
from typing import Optional
from urllib.parse import urljoin
from pydantic import Field


class WorkerContractResponse(Response):
    code: int
    status: str
    job_id: Optional[str] = Field(alias="job", default=None)

    def from_response(response: httpx.Response):
        return WorkerContractResponse(**response.json())


class WorkerContractRequest(Request[WorkerContractResponse]):
    worker_id: str = Field(serialization_alias="id")
    tags: list[str]
    timeout: int

    def endpoint(self):
        return f"worker/{self.worker_id}/contract"

    async def send(
        self,
        client: httpx.AsyncClient,
        host: str,
    ) -> WorkerContractResponse:
        url = urljoin(host, self.endpoint())
        response = await client.post(url, json=self.model_dump(by_alias=True))

        return WorkerContractResponse.from_response(response)
