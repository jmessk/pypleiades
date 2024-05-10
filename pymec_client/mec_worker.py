from typing import Optional
from typing_extensions import Self
import logging

from .api import worker_api
from .mec_object import MECObject
from .mec_job import MECJob


class MECWorker(MECObject):
    __slots__ = ["_server_url", "_id", "_logger", "_runtimes", "_tags"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            server_url=server_url,
            logger=logger,
        )

        self._runtimes: Optional[list[str]] = None
        self._tags: list[str] = []

    # properties

    @property
    def runtimes(self) -> list[str]:
        if self._runtimes is None:
            raise ValueError("runtimes is not set")
        return self._runtimes

    @property
    def tags(self) -> list[str]:
        return self._tags

    # info

    def remote_info(self) -> worker_api.RespWorkerInfo:
        if not self.has_remote():
            raise Exception()

        result = worker_api.info(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    async def remote_info_async(self) -> worker_api.RespWorkerInfo:
        if not self.has_remote():
            raise Exception()

        result = await worker_api.info_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    # runtimes

    def set_runtimes(self, runtimes: list[str]) -> Self:
        if self.has_remote():
            raise Exception()

        self._runtimes = runtimes

        return self

    # register

    def register(self) -> Self:
        if self.has_remote():
            raise Exception()

        result = worker_api.register(self._server_url, self._runtimes)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().worker_id

        return self

    async def register_async(self) -> Self:
        if self.has_remote():
            raise Exception()

        result = await worker_api.register_async(self._server_url, self._runtimes)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().worker_id

        return self

    # tags

    def set_tags(self, tags: list[str]) -> Self:
        self._tags = tags

        return self

    # contract

    def contract(self, timeout: int = 20) -> MECJob:
        if not self.has_remote():
            raise Exception()

        result = worker_api.contract(self._server_url, self._id, self._tags, timeout)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return MECJob(
            self._server_url,
            job_id=result.unwrap().job_id,
            logger=self._logger,
        ).download()

    async def contract_async(self, timeout: int = 20) -> MECJob:
        if not self.has_remote():
            raise Exception()

        result = await worker_api.contract_async(
            self._server_url,
            self._id,
            self._tags,
            timeout,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return await MECJob(
            self._server_url,
            job_id=result.unwrap().job_id,
            logger=self._logger,
        ).download_async()
