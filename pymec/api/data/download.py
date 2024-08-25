from ..api_types import Request, Response
import httpx
from urllib.parse import urljoin


class DataDownloadResponse(Response):
    data: bytes

    def from_response(response: httpx.Response):
        return DataDownloadResponse(data=response.content)


class DataDownloadRequest(Request[DataDownloadResponse]):
    data_id: str

    def endpoint(self):
        return f"data/{self.data_id}/blob"

    async def send(self, client: httpx.AsyncClient, host: str) -> DataDownloadResponse:
        url = urljoin(host, self.endpoint())
        response = await client.get(url)

        return DataDownloadResponse.from_response(response)
