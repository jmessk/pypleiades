from ..api_types import Request, Response
import httpx
from urllib.parse import urljoin
import io
from pydantic import Field


class DataUploadResponse(Response):
    code: int
    status: str
    data_id: str = Field(alias="id")
    checksum: str

    def from_response(response: httpx.Response):
        return DataUploadResponse(**response.json())


class DataUploadRequest(Request[DataUploadResponse]):
    data: bytes

    def endpoint(self):
        return "data"

    async def send(self, client: httpx.AsyncClient, host: str) -> DataUploadResponse:
        blob = {"file": ("input", io.BytesIO(self.data))}

        url = urljoin(host, self.endpoint())
        response = await client.post(url, files=blob)

        return DataUploadResponse.from_response(response)
