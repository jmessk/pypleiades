from ..api_types import Request, Response
import httpx
from typing import override
from urllib.parse import urljoin
import io
from pydantic import Field


class DataUploadResponse(Response):
    code: int
    status: str
    data_id: str = Field(alias="id")
    checksum: str

    @override
    def from_response(response: httpx.Response):
        return DataUploadResponse(**response.json())


class DataUploadRequest(Request):
    data: bytes

    @override
    def endpoint(self):
        return "data"

    @override
    async def send(self, client: httpx.AsyncClient, host: str) -> DataUploadResponse:
        blob = {"file": ("input", io.BytesIO(self.data))}

        url = urljoin(host, self.endpoint())
        response = await client.post(url, files=blob)

        return DataUploadResponse.from_response(response)
