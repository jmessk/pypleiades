from httpx import AsyncClient

from . import download, upload


class Data:
    __slots__ = ["__client"]

    def __init__(self, client: AsyncClient) -> None:
        self.__client = client

    async def download(self, data_id: str) -> download.Response:
        await download.Request(data_id=data_id).send(self.__client)

    async def upload(self, data: bytes) -> upload.Response:
        await upload.Request(data=data).send(self.__client)
