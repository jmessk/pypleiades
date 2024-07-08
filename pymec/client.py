from .api import api_types

from httpx import AsyncClient
from typing import Optional, Self


class Client:
    __slots__ = ["_client", "_host"]

    def __init__(self):
        self._client: Optional[AsyncClient] = None
        self._host: Optional[str] = None

    def client(self, client: AsyncClient) -> Self:
        self._client = client
        return self

    def host(self, host: str) -> Self:
        self._host = host
        return self

    async def request(self, request: api_types.Request) -> api_types.Response:
        return await request.send(self._client, self._host)
