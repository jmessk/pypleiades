from .api import Api

from httpx import AsyncClient
from typing import Optional


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
    __slots__ = ["__client"]

    def __init__(self):
        self.__client: Optional[AsyncClient] = None
        self.__api = Api(self.__client)

    def builder(self) -> ClientBuilder:
        return ClientBuilder()

    @property
    def api(self) -> Api:
        return self.__api
