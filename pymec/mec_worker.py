from typing import Optional
from typing_extensions import Self
import logging

from .api import worker_api
from .mec_object import MECObject
from .mec_job import MECJob


class MECWorker(MECObject):
    __slots__ = [
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
        "_worker_api",
        "_runtimes",
        "_tags",
    ]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(
            server_url=server_url,
            logger=logger,
            httpx_config=httpx_config,
        )

        self._worker_api = worker_api.WorkerAPI(
            self._server_url,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._runtimes: Optional[list[str]] = None
        self._tags: list[str] = []

    # properties

    @property
    def runtimes(self) -> Optional[list[str]]:
        return self._runtimes

    @property
    def tags(self) -> list[str]:
        return self._tags

    # info

    def remote_info(self) -> worker_api.RespWorkerInfo:
        if not self.has_remote():
            raise Exception()

        result = self._worker_api.info(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()
        
        self._logger.info("Fetched remote worker info.")

        return result.unwrap()

    async def remote_info_async(self) -> worker_api.RespWorkerInfo:
        if not self.has_remote():
            raise Exception()

        result = await self._worker_api.info_async(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()
        
        self._logger.info("Fetched remote worker info.")

        return result.unwrap()

    # runtimes

    def set_runtimes(self, runtimes: list[str]) -> Self:
        if self.has_remote():
            raise Exception()

        self._runtimes = runtimes
        self._logger.info(f"Set worker runtimes: {self._runtimes}")

        return self

    # register

    def register(self) -> Self:
        if self.has_remote():
            raise Exception()

        result = self._worker_api.register(self._runtimes)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().worker_id
        self._logger.info(f"Registered worker: {self._id}")

        return self

    async def register_async(self) -> Self:
        if self.has_remote():
            raise Exception()

        result = await self._worker_api.register_async(self._runtimes)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().worker_id
        self._logger.info(f"Registered worker: {self._id}")

        return self

    # tags

    def set_tags(self, tags: list[str]) -> Self:
        self._tags = tags
        self._logger.info(f"Set worker tags: {self._tags}")

        return self

    # contract

    def contract(self, timeout: int = 20) -> Optional[MECJob]:
        if not self.has_remote():
            raise Exception()
        
        self._logger.info("Contracting job.")

        result = self._worker_api.contract(self._id, self._tags, timeout)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        response = result.unwrap()

        if response.job_id is None:
            self._logger.info("No job to contract.")
            return None
        
        self._logger.info(f"Contracted job: {response.job_id}")

        return MECJob(
            self._server_url,
            id=response.job_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        ).fetch_meta()

    async def contract_async(self, timeout: int = 20) -> Optional[MECJob]:
        if not self.has_remote():
            raise Exception()

        result = await self._worker_api.contract_async(
            self._id,
            self._tags,
            timeout,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        response = result.unwrap()

        if response.job_id is None:
            self._logger.info("No job to contract.")
            return None
        
        self._logger.info(f"Contracted job: {response.job_id}")

        return await MECJob(
            self._server_url,
            job_id=response.job_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        ).fetch_meta_async()

    # wait contract

    def wait_contract(self, timeout: int = 20) -> MECJob:
        while True:
            if (job := self.contract(timeout)) is not None:
                return job

    async def wait_contract_async(self, timeout: int = 20) -> MECJob:
        while True:
            if (job := await self.contract_async(timeout)) is not None:
                return job
