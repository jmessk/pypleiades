from ..api_types import Request, Response
import httpx
from overrides import override
from urllib.parse import urljoin


class DataDownloadResponse(Response):
    data: bytes

    @override
    def from_response(response: httpx.Response):
        return DataDownloadResponse(data=response.content)


class DataDownloadRequest(Request):
    data_id: str

    @override
    def endpoint(self):
        return f"data/{self.data_id}/blob"

    @override
    async def send(self, client: httpx.AsyncClient, host: str) -> DataDownloadResponse:
        url = urljoin(host, self.endpoint())
        response = await client.get(url)

        return DataDownloadResponse.from_response(response)
