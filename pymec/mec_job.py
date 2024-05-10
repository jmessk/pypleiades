from typing import Optional
from typing_extensions import Self
import logging

from .api import job_api
from .mec_object import MECObject
from .mec_blob import MECBlob
from .mec_lambda import MECLambda


class MECJob(MECObject):
    __slots__ = ["_server_url", "_id", "_logger", "_input", "_lambda", "_tags"]

    def __init__(
        self,
        server_url: str,
        id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            server_url=server_url,
            id=id,
            logger=logger,
        )

        self._input: Optional[MECBlob] = None
        self._lambda: Optional[MECLambda] = None
        self._tags: list[str] = []

    # properties

    @property
    def input(self) -> MECBlob:
        if self._input is None:
            raise ValueError("input is not set")
        return self._input

    @property
    def lambda_(self) -> MECLambda:
        if self._lambda is None:
            raise ValueError("lambda is not set")
        return self._lambda

    @property
    def tags(self) -> list[str]:
        if self._tags is None:
            raise ValueError("tags is not set")
        return self._tags

    # info

    def remote_info(self) -> job_api.RespJobInfo:
        if not self.has_remote():
            raise Exception()

        result = job_api.info(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    async def remote_info_async(self) -> job_api.RespJobInfo:
        if not self.has_remote():
            raise Exception()

        result = await job_api.info_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    # blob

    def set_input(self, blob: MECBlob) -> Self:
        if self.has_remote():
            raise Exception()

        if self._input is not None:
            raise Exception()

        self._input = blob

        return self

    # lambda

    def set_lambda(self, lambda_: MECLambda):
        if self.has_remote():
            raise Exception()

        if self._lambda is not None:
            raise Exception()

        self._lambda = lambda_

        return self

    # tags

    def set_tags(self, tags: list[str]) -> Self:
        if self.has_remote():
            raise Exception()

        self._tags = tags

        return self

    # run

    def run(self) -> Self:
        if self.has_remote():
            raise Exception()

        if self._input is None:
            raise ValueError("input is not set")

        if self._lambda is None:
            raise ValueError("lambda is not set")

        if not self._input.has_remote():
            self._input.upload()

        if not self._lambda.has_remote():
            self._lambda.upload()

        result = job_api.create_job(
            self._server_url,
            self._lambda.id,
            self._input.id,
            self._tags,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().job_id

        return self

    async def run_async(self) -> Self:
        if self.has_remote():
            raise Exception()

        if self._input is None:
            raise ValueError("input is not set")

        if self._lambda is None:
            raise ValueError("lambda is not set")

        if not self._input.has_remote():
            await self._input.upload_async()

        if not self._lambda.has_remote():
            await self._lambda.upload_async()

        result = await job_api.create_job_async(
            self._server_url,
            self._lambda.id,
            self._input.id,
            self._tags,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().job_id

        return self

    # is finished

    def is_finished(self) -> bool:
        if not self.has_remote():
            raise Exception()

        result = job_api.info(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap().state == "Finished"

    async def is_finished_async(self) -> bool:
        if not self.has_remote():
            raise Exception()

        result = await job_api.info_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap().state == "Finished"

    # download

    def download(self) -> Self:
        if not self.has_remote():
            raise Exception()

        info = self.remote_info()

        self._input = MECBlob(
            self._server_url, info.input_data_id, self._logger
        ).download()

        self._lambda = MECLambda(
            self._server_url, info.lambda_id, self._logger
        ).download()

        return self

    async def download_async(self) -> Self:
        if not self.has_remote():
            raise Exception()

        info = await self.remote_info_async()

        self._input = await MECBlob(
            self._server_url, info.input_data_id, self._logger
        ).download_async()

        self._lambda = await MECLambda(
            self._server_url, info.lambda_id, self._logger
        ).download_async()

        return self

    # finish

    def finish(self, blob: MECBlob) -> Self:
        if not self.has_remote():
            raise Exception()

        if not blob.has_remote():
            blob.upload()

        result = job_api.update_status(self._server_url, self._id, blob.id, "finished")

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return self

    async def finish_async(self, blob: MECBlob) -> Self:
        if not self.has_remote():
            raise Exception()

        if not blob.has_remote():
            await blob.upload_async()

        result = await job_api.update_status_async(
            self._server_url,
            self._id,
            blob.id,
            "finished",
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return self
