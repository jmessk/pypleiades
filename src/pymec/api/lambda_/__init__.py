from .create import Request as Create

from httpx import AsyncClient

from . import create
from .create import Request as Create


class Lambda:
    __slots__ = ["_client"]

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create(
        self,
        data_id: str,
        runtime: str,
    ) -> create.Response:
        return await create.Request(data_id=data_id, runtime=runtime).send(self._client)
