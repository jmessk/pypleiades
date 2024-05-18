from typing import Optional
from typing_extensions import Self
import logging

from .api import lambda_api
from .mec_object import MECObject
from .mec_blob import MECBlob


# class MECLambdaException(Exception):
#     def __init__(self, message: str):
#         super().__init__(message)


class MECLambda(MECObject):
    __slots__ = [
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
        "_lambda_api",
        "_blob",
        "_runtime",
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

        self._lambda_api = lambda_api.LambdaAPI(
            self._server_url,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._blob: Optional[MECBlob] = None
        self._runtime: Optional[str] = None

    # checker

    def has_blob(self) -> bool:
        return self._blob is not None

    def has_runtime(self) -> bool:
        return self._runtime is not None

    # blob

    # get

    def get_blob(self) -> MECBlob:
        if not self.has_blob():
            raise Exception()

        return self._blob

    async def get_blob_async(self) -> MECBlob:
        if not self.has_blob():
            raise Exception()

        return self._blob

    # set

    def set_blob(self, blob: MECBlob) -> Self:
        if self.has_blob():
            raise Exception()

        self._blob = blob
        self._logger.info("Set lambda code.")

        return self

    # runtime

    def get_runtime(self) -> str:
        if not self.has_runtime():
            raise Exception()

        return self._runtime

    def set_runtime(self, runtime: str) -> Self:
        if self.has_runtime():
            raise Exception()

        self._runtime = runtime
        self._logger.info(f"Set lambda runtime: {self._runtime} .")

        return self

    # info

    def remote_info(self) -> lambda_api.RespLambdaInfo:
        if not self.has_remote():
            raise Exception()

        result = self._lambda_api.info(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._logger.info("Fetched remote lambda info.")

        return result.unwrap()

    async def remote_info_async(self) -> lambda_api.RespLambdaInfo:
        if not self.has_remote():
            raise Exception()

        result = await self._lambda_api.info_async(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._logger.info("Fetched remote lambda info.")

        return result.unwrap()

    # upload

    def upload(self) -> Self:
        if self.has_remote():
            raise Exception()

        if not self.has_blob():
            raise Exception()

        if not self.has_runtime():
            raise Exception()

        if not self._blob.has_remote():
            self._blob.upload()

        result = self._lambda_api.create(
            self._blob.id,
            self._runtime,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().lambda_id
        self._logger.info(f"Uploaded lambda to {self._id} .")

        return self

    async def upload_async(self) -> Self:
        if self.has_remote():
            raise Exception()

        if not self.has_blob():
            raise Exception()

        if not self.has_runtime():
            raise Exception()

        if not self._blob.has_remote():
            await self._blob.upload_async()

        result = await self._lambda_api.create_async(
            self._blob.id,
            self._runtime,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().lambda_id
        self._logger.info(f"Uploaded lambda to {self._id} .")

        return self

    # fetch

    def fetch(self) -> Self:
        if not self.has_remote():
            raise Exception()

        # if self._blob is not None:
        if self.has_blob():
            raise Exception()

        info = self.remote_info()

        self._blob = MECBlob(
            self._server_url,
            id=info.data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._runtime = info.runtime

        self._logger.info(f"Downloaded lambda from {self._id} .")

        return self

    async def fetch_async(self) -> Self:
        if not self.has_remote():
            raise Exception()

        if self.has_blob():
            raise Exception()

        info = await self.remote_info_async()

        self._blob = await MECBlob(
            self._server_url,
            id=info.data_id,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._runtime = info.runtime

        self._logger.info(f"Downloaded lambda from {self._id} .")

        return self
