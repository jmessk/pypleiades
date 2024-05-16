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

    # checker

    def has_input(self) -> bool:
        return self._input_blob is not None

    def has_output(self) -> bool:
        return self._output_blob is not None

    def has_lambda(self) -> bool:
        return self._lambda is not None

    def has_tags(self) -> bool:
        return self._tags is not None

    # input

    def set_input(self, blob: MECBlob) -> Self:
        self._input_blob = blob
        self._logger.info("Set input blob.")

        return self

    def get_input(self) -> MECBlob:
        if not self.has_input():
            raise ValueError("input is not set")
        return self._input_blob

    # output

    def get_output(self) -> MECBlob:
        if not self.has_output():
            raise ValueError("output is not set")
        return self._output_blob

    # lambda

    def set_lambda(self, lambda_: MECLambda) -> Self:
        if self.has_lambda():
            raise Exception()

        self._lambda = lambda_
        self._logger.info(f"Set lambda: {self._lambda.get_runtime()} .")

        return self

    def get_lambda(self) -> MECLambda:
        if not self.has_lambda():
            raise ValueError("lambda is not set")
        return self._lambda

    # tags

    def set_tags(self, tags: list[str]) -> Self:
        self._tags = tags
        self._logger.info(f"Set job tags: {self._tags}")

        return self

    # def get_tags(self) -> list[str]:

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

    # run

    def run(self) -> Self:
        if not self.has_input():
            raise ValueError("input is not set")

        if not self.has_lambda():
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
        if not self.has_input():
            raise ValueError("input is not set")

        if not self.has_lambda():
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
        self.wait("", 0)
        return self.has_output()

    async def is_finished_async(self) -> bool:
        await self.wait_async("", 0)
        return self.has_output()

    # wait finish

    def wait(self, except_status: str, sec: int) -> Self:
        if not self.has_remote():
            raise Exception()

        result_info = self._job_api.info(
            self._id,
            except_status=except_status,
            timeout_s=sec,
        )

        if result_info.is_err():
            self._logger.error(result_info.unwrap_err())
            raise Exception()

        if result_info.unwrap().job_status != "Finished":
            raise Exception()

        output_data_id = result_info.unwrap().output.data_id

        self._output_blob = MECBlob(
            self._server_url,
            id=output_data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._logger.info(f"Job is finished: {self._id}")

        return self

    async def wait_async(self, except_status: str, sec: int) -> Self:
        if not self.has_remote():
            raise Exception()

        result_info = await self._job_api.info_async(
            self._id,
            except_status=except_status,
            timeout_s=sec,
        )

        if result_info.is_err():
            self._logger.error(result_info.unwrap_err())
            raise Exception()

        if result_info.unwrap().job_status != "Finished":
            raise Exception()

        output_data_id = result_info.unwrap().output.data_id

        self._output_blob = MECBlob(
            self._server_url,
            id=output_data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._logger.info(f"Job is finished: {self._id}")

        return self

    # fetch meta

    def fetch(self) -> Self:
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

        self._logger.info("Fetched job: {self._id}")

        return self

    async def fetch_async(self) -> Self:
        if not self.has_remote():
            raise Exception()

        info = await self.remote_info_async()

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

        self._logger.info("Fetched job: {self._id}")

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
