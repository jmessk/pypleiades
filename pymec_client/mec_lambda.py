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
    __slots__ = ["_server_url", "_id", "_logger", "_blob", "_runtime"]

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

        self._blob: Optional[MECBlob] = None

    # properties

    @property
    def _blob(self) -> MECBlob:
        if self._blob is None:
            raise ValueError("blob is not set")
        return self._blob

    @property
    def runtime(self) -> str:
        if self._runtime is None:
            raise ValueError("runtime is not set")
        return self._runtime

    # info

    def remote_info(self) -> lambda_api.RespLambdaInfo:
        if not self.has_remote():
            raise Exception()

        result = lambda_api.info(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    async def remote_info_async(self) -> lambda_api.RespLambdaInfo:
        if not self.has_remote():
            raise Exception()

        result = await lambda_api.info_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    # code

    def set_code(self, blob: MECBlob) -> Self:
        if self.has_remote():
            raise Exception()

        if self._blob is not None:
            raise Exception()

        self._blob = blob

        return self

    # runtime

    def set_runtime(self, runtime: str) -> Self:
        if self.has_remote():
            raise Exception()

        if self._runtime is not None:
            raise Exception()

        self._runtime = runtime

        return self

    # upload

    def upload(self) -> Self:
        if self.has_remote():
            raise Exception()

        if self._blob is None:
            raise Exception()

        if self._runtime is None:
            raise Exception()
        
        if not self._blob.has_remote():
            self._blob.upload()

        result = lambda_api.create(
            self._server_url,
            self._blob.id,
            self._runtime,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().lambda_id

        return self

    async def upload_async(self) -> Self:
        if self.has_remote():
            raise Exception()

        if self._blob is None:
            raise Exception()

        if self._runtime is None:
            raise Exception()

        result = await lambda_api.create_async(
            self._server_url,
            self._blob.id,
            self._runtime,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        self._id = result.unwrap().lambda_id

        return self

    # download

    def download(self) -> Self:
        if not self.has_remote():
            raise Exception()

        if self._blob is not None:
            raise Exception()

        info = self.remote_info()

        self._blob = MECBlob(
            self._server_url,
            id=info.data_id,
            logger=self._logger,
        ).download()

        return self

    async def download_async(self) -> Self:
        if not self.has_remote():
            raise Exception()

        if self._blob is not None:
            raise Exception()

        info = await self.remote_info_async()

        self._blob = await MECBlob(
            self._server_url,
            id=info.data_id,
            logger=self._logger,
        ).download_async()

        return self
