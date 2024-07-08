from ..api_types import Request, Response
import httpx
from typing import override
from urllib.parse import urljoin
from pydantic import Field


class JobUpdateResponse(Response):
    code: int
    status: str
    message: str

    @override
    def from_response(response: httpx.Response):
        return JobUpdateResponse(**response.json())


class JobUpdateRequest(Request):
    job_id: str = Field(exclude=True)
    data_id: str = Field(serialization_alias="output")
    status: str = Field(serialization_alias="status")

    @override
    def endpoint(self):
        return f"job/{self.job_id}"

    @override
    async def send(self, client: httpx.AsyncClient, host: str) -> JobUpdateResponse:
        url = urljoin(host, self.endpoint())
        response = await client.post(url, json=self.model_dump())

        return JobUpdateResponse.from_response(response)
