from .api import type
from .api import Api

from httpx import AsyncClient
from typing import Optional, TypeVar


R = TypeVar("R", bound=type.Response)


class ClientBuilder:
    def __init__(self):
        self.__client: Optional[AsyncClient] = None
        self.__host: Optional[str] = None

    def client(self, client: AsyncClient) -> "ClientBuilder":
        if self.__client is not None:
            raise ValueError("Client is already set")

        if client.base_url is not None:
            self.__host = client.base_url

        self.__client = client

        return self

    def host(self, host: str) -> "ClientBuilder":
        if self.__host is not None:
            raise ValueError("Host is already set")

        self.__host = host

        return self

    def build(self) -> "Client":
        if self.__client is None:
            self.__client = AsyncClient(timeout=30)

        if self.__host is None:
            raise ValueError("Host is not set")

        self.__client.base_url = self.__host

        return Client(self.__client)


class Client:
    __slots__ = ["__client", "_api"]

    def __init__(self, client: AsyncClient):
        self.__client = client
        self._api = Api(self.__client)

    @property
    def api(self) -> Api:
        return self._api
    
    @staticmethod
    def builder() -> ClientBuilder:
        return ClientBuilder()

    async def call_api(self, request: type.Request[R]) -> R:
        return await request.send(self.__client)
