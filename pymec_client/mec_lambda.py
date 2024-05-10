from typing import Optional
from typing_extensions import Self
import aiofiles
import logging

from mec_object import MECObject
from pleiades_api import lambda_api
from mec_blob import MECBlob


# class MECLambdaException(Exception):
#     def __init__(self, message: str):
#         super().__init__(message)


class MECLambda(MECObject):
    __slots__ = ["_server_url", "_id", "_logger", "_code_blob"]

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

    # properties

    # info

    def info(self) -> lambda_api.RespLambdaInfo:
        if self._id is None:
            raise Exception()

        result = lambda_api.get_lambda_info(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()
    
    async def info_async(self) -> lambda_api.RespLambdaInfo:
        if self._id is None:
            raise Exception()
        
        result = await lambda_api.get_lambda_info_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception()

        return result.unwrap()

    # code

    def set_code(self, blob: MECBlob):
        if self._code_blob is not None:
            raise Exception()

        self._code_blob = blob

        return self
    
    # runtime

    def set_runtime(self, runtime: str):
        if self._runtime is not None:
            raise Exception()

        self._runtime = runtime

        return self

    # 