from .download import Request as Download
from .upload import Request as Upload

from httpx import AsyncClient

from . import download, upload


class Data:
    __slots__ = ["_client"]

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def download(self, data_id: str) -> download.Response:
        return await download.Request(data_id=data_id).send(self._client)

    async def upload(self, data: bytes) -> upload.Response:
        return await upload.Request(data=data).send(self._client)
