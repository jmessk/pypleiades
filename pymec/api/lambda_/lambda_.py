from httpx import AsyncClient

from . import create


class Lambda:
    __slots__ = ["__client"]

    def __init__(self, client: AsyncClient) -> None:
        self.__client = client

    async def create(
        self,
        data_id: str,
        runtime: str,
    ) -> create.Response:
        await create.Request(data_id=data_id, runtime=runtime).send(self.__client)
