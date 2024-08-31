from httpx import AsyncClient

from . import create, info, update


class Job:
    __slots__ = ["__client"]

    def __init__(self, client: AsyncClient) -> None:
        self.__client = client

    async def create(
        self,
        lambda_id: str,
        input_id: str,
        tags: list[str] = [],
    ) -> create.Response:
        await create.Request(
            lambda_id=lambda_id,
            data_id=input_id,
            tags=tags,
        ).send(self.__client)

    async def info(
        self,
        job_id: str,
        except_: str | None = None,
        timeout: str | None = None,
    ) -> info.Response:
        await info.Request(
            job_id=job_id,
            except_=except_,
            timeout=timeout,
        ).send(self.__client)

    async def update(self, job_id: str, output_id: str, status: str) -> update.Response:
        await update.Request(
            job_id=job_id,
            data_id=output_id,
            status=status,
        ).send(self.__client)
