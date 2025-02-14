from .register import Request as Register
from .contract import Request as Contract

from httpx import AsyncClient

from . import register, contract


class Worker:
    __slots__ = ["_client"]

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def register(self, runtimes: list[str]) -> register.Response:
        return await register.Request(runtimes=runtimes).send(self._client)

    async def contract(
        self,
        worker_id: str,
        timeout: int,
        tags: list[str] = [],
    ) -> contract.Response:
        return await contract.Request(
            worker_id=worker_id,
            tags=tags,
            timeout=timeout,
        ).send(self._client)
