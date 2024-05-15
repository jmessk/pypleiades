from typing import Optional
from typing_extensions import Self
import logging
import time
import asyncio

from .api import job_api
from .mec_object import MECObject
from .mec_blob import MECBlob
from .mec_lambda import MECLambda


class MECJob(MECObject):
    __slots__ = [
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
        "_job_api",
        "_input_blob",
        "_output_blob",
        "_lambda",
        "_tags",
    ]

    def __init__(
        self,
        server_url: str,
        id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        super().__init__(
            server_url=server_url,
            id=id,
            logger=logger,
            httpx_config=httpx_config,
        )

        self._job_api = job_api.JobAPI(
            self._server_url,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._input_blob: Optional[MECBlob] = None
        self._output_blob: Optional[MECBlob] = None
        self._lambda: Optional[MECLambda] = None
        self._tags: list[str] = []

    # properties

    @property
    def input(self) -> Optional[MECBlob]:
        if self._input_blob.has_remote() and self._input_blob.data is None:
            self._input_blob.download()
        return self._input_blob

    @property
    async def input_async(self) -> MECBlob:
        if self._input_blob.has_remote() and self._input_blob.data is None:
            await self._input_blob.download_async()
        return self._input_blob

    @property
    def output(self) -> MECBlob:
        if self._output_blob is None:
            raise ValueError("output is not set.")

        if self._output_blob.has_remote() and self._output_blob.data is None:
            self._output_blob.download()

        return self._output_blob

    @property
    async def output_async(self) -> MECBlob:
        if self._output_blob is None:
            raise ValueError("output is not set.")

        if self._output_blob.has_remote() and self._output_blob.data is None:
            await self._output_blob.download_async()

        return self._output_blob

    @property
    def lambda_(self) -> MECLambda:
        if self._lambda is None:
            raise ValueError("lambda is not set.")

        if self._lambda.has_remote() and self._lambda.blob is None:
            self._lambda.download()

        return self._lambda

    @property
    async def lambda_async(self) -> MECLambda:
        if self._lambda is None:
            raise ValueError("lambda is not set.")

        if self._lambda.has_remote() and self._lambda.blob is None:
            await self._lambda.download_async()

        return self._lambda

    @property
    def tags(self) -> list[str]:
        if self._tags is None:
            raise ValueError("tags is not set.")
        return self._tags

    # info

    def remote_info(self) -> job_api.RespJobInfo:
        if not self.has_remote():
            raise Exception()

        result = self._job_api.info(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._logger.info("Fetched remote Job info.")

        return result.unwrap()

    async def remote_info_async(self) -> job_api.RespJobInfo:
        if not self.has_remote():
            raise Exception()

        result = await self._job_api.info_async(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._logger.info("Fetched remote Job info.")

        return result.unwrap()

    # blob

    def set_input(self, blob: MECBlob) -> Self:
        if self.has_remote():
            raise Exception()

        if self._input_blob is not None:
            raise Exception()

        self._input_blob = blob
        self._logger.info("Set input blob.")

        return self

    # lambda

    def set_lambda(self, lambda_: MECLambda):
        if self.has_remote():
            raise Exception()

        if self._lambda is not None:
            raise Exception()

        self._lambda = lambda_
        self._logger.info(f"Set lambda: {self._lambda.runtime} .")

        return self

    # tags

    def set_tags(self, tags: list[str]) -> Self:
        if self.has_remote():
            raise Exception()

        self._tags = tags
        self._logger.info(f"Set job tags: {self._tags}")

        return self

    # run

    def run(self) -> Self:
        if self.has_remote():
            raise Exception()

        if self._input_blob is None:
            raise ValueError("input is not set")

        if self._lambda is None:
            raise ValueError("lambda is not set")

        if not self._input_blob.has_remote():
            self._input_blob.upload()

        if not self._lambda.has_remote():
            self._lambda.upload()

        result = self._job_api.create(
            self._lambda.id,
            self._input_blob.id,
            self._tags,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().job_id
        self._logger.info(f"Created job: {self._id}")

        return self

    async def run_async(self) -> Self:
        if self.has_remote():
            raise Exception()

        if self._input_blob is None:
            raise ValueError("input is not set")

        if self._lambda is None:
            raise ValueError("lambda is not set")

        if not self._input_blob.has_remote():
            await self._input_blob.upload_async()

        if not self._lambda.has_remote():
            await self._lambda.upload_async()

        result = await self._job_api.create_async(
            self._lambda.id,
            self._input_blob.id,
            self._tags,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().job_id
        self._logger.info(f"Created job: {self._id}")

        return self

    # is finished

    def is_finished(self) -> bool:
        if not self.has_remote():
            raise Exception()

        result = self._job_api.info(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        if result.unwrap().job_status != "Finished":
            return False

        output_data_id = result.unwrap().output.data_id

        self._output_blob = MECBlob(
            self._server_url,
            id=output_data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._logger.info(f"Job is finished: {self._id}")

        return True

    async def is_finished_async(self) -> bool:
        if not self.has_remote():
            raise Exception()

        result_info = await self._job_api.info_async(self._id)

        if result_info.is_err():
            self._logger.error(result_info.unwrap_err())
            raise Exception()

        if result_info.unwrap().job_status != "Finished":
            return False

        output_data_id = result_info.unwrap().output.data_id

        self._output_blob = await MECBlob(
            self._server_url,
            id=output_data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._logger.info(f"Job is finished: {self._id}")

        return True

    # wait for finish

    def wait_for_finish(self, sleep_s=0.0) -> Self:
        self._logger.info(f"Waiting for job to finish: {self._id}")

        while not self.is_finished():
            time.sleep(sleep_s)

        return self

    async def wait_for_finish_async(self, sleep_s=0.0) -> Self:
        self._logger.info(f"Waiting for job to finish: {self._id}")

        while not await self.is_finished_async():
            await asyncio.sleep(sleep_s)

        return self

    # fetch meta

    def fetch_meta(self) -> Self:
        if not self.has_remote():
            raise Exception()

        info = self.remote_info()

        self._input_blob = MECBlob(
            self._server_url,
            id=info.input.data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._lambda = MECLambda(
            self._server_url,
            id=info.lambda_.lambda_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._logger.info("Downloaded job: {self._id}")

        return self

    async def fetch_meta_async(self) -> Self:
        if not self.has_remote():
            raise Exception()

        info = await self.remote_info_async()

        self._input_blob = await MECBlob(
            self._server_url,
            id=info.input.data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._lambda = await MECLambda(
            self._server_url,
            id=info.lambda_.lambda_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._logger.info("Downloaded job: {self._id}")

        return self

    # finish

    def finish(self, blob: MECBlob) -> Self:
        if not self.has_remote():
            raise Exception()

        if not blob.has_remote():
            blob.upload()

        result = self._job_api.update(self._id, blob.id, "finished")

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._logger.info(f"Finished job: {self._id}")

        return self

    async def finish_async(self, blob: MECBlob) -> Self:
        if not self.has_remote():
            raise Exception()

        if not blob.has_remote():
            await blob.upload_async()

        result = await self._job_api.update_async(
            self._id,
            blob.id,
            "finished",
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._logger.info(f"Finished job: {self._id}")

        return self
