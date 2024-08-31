from httpx import AsyncClient

from . import register, contract


class Worker:
    __slots__ = ["__client"]

    def __init__(self, client: AsyncClient) -> None:
        self.__client = client

    async def register(self, runtimes: list[str]) -> register.Response:
        await register.Request(runtimes=runtimes).send(self.__client)

    async def contract(
        self,
        worker_id: str,
        timeout: int,
        tags: list[str] = [],
    ) -> contract.Response:
        await contract.Request(
            worker_id=worker_id,
            tags=tags,
            timeout=timeout,
        ).send(self.__client)
