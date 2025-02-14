from .api import Api, ping, type

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
    __slots__ = ["__client", "__api"]

    def __init__(self, client: AsyncClient):
        self.__client = client
        self.__api = Api(self.__client)

    @staticmethod
    def default() -> "Client":
        import os

        url = os.environ.get("PLEIADES_URL")
        if url is None:
            raise ValueError("PLEIADES_URL is not set")

        return ClientBuilder().host(url).build()

    @staticmethod
    def builder() -> ClientBuilder:
        return ClientBuilder()

    @property
    def api(self) -> Api:
        return self.__api

    async def call_api(self, request: type.Request[R]) -> R:
        return await request.send(self.__client)

    async def ping(self) -> ping.Response:
        return await self.call_api(ping.Request())
