from typing import Optional
from typing_extensions import Self
import aiofiles
import logging

from mec_object import MECObject
from pleiades_api import data_api


class MECBlobException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECBlob(MECObject):
    __slots__ = ["_server_url", "_id", "_logger", "_data"]

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

        self._data: Optional[bytes] = None

    # properties

    @property
    def data(self) -> bytes:
        return self._data
    
    # info

    def info(self) -> data_api.RespDataInfo:
        if self._id is None:
            raise MECBlobException("No data to get info")

        result = data_api.get_data_info(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to get data info")

        return result.unwrap()
    
    async def info_async(self) -> data_api.RespDataInfo:
        if self._id is None:
            raise MECBlobException("No data to get info")
        
        result = await data_api.get_data_info_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to get data info")
        
        return result.unwrap()

    # from bytes

    def from_bytes(self, data: bytes) -> Self:
        if self._data is not None:
            raise MECBlobException("Data already exists")

        self._data = data

        return self

    # from file

    def from_file(self, file_path: str) -> Self:
        with open(file_path, "rb") as file:
            self._data = file.read()

        self._logger.info(f"Loaded data from {file_path}")

        return self

    async def from_file_async(self, file_path: str) -> Self:
        async with aiofiles.open(file_path, "rb") as file:
            self._data = await file.read()

        self._logger.info(f"Loaded data from {file_path}")

        return self

    # save as file

    def save(self, file_path: str) -> Self:
        with open(file_path, "wb") as file:
            file.write(self._data)

        self._logger.info(f"Saved data to {file_path}")

        return self

    async def save_async(self, file_path: str) -> Self:
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(self._data)

        self._logger.info(f"Saved data to {file_path}")

        return self

    # upload

    def upload(self) -> Self:
        if self._id is not None:
            raise MECBlobException("Data already exists on remote server")

        if self._data is None:
            raise MECBlobException("No data to upload")

        result = data_api.post_data(self._server_url, self._data)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to upload data")

        self._id = result.unwrap()
        self._logger.info(f"Uploaded data to {self._id}")

        return self

    async def upload_async(self) -> Self:
        if self._id is not None:
            raise MECBlobException("Data already exists on remote server")

        if self._data is None:
            raise MECBlobException("No data to upload")

        result = await data_api.post_data_async(self._server_url, self._data)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to upload data")

        self._id = result.unwrap()
        self._logger.info(f"Uploaded data to {self._id}")

        return self

    # download
    # __init__ では async は使えないので、別途関数を用意する。
    # 自動的にダウンロードするのではなく、明示的にダウンロードするようにする。
    # そのほうがユーザが意図しないタイミングでのダウンロードを防げる。

    def download(self) -> Self:
        if self._id is None:
            raise MECBlobException("No data to download")

        if self._data is not None:
            raise MECBlobException("This object already contains data")

        result = data_api.get_data(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to download data")

        self._data = result.unwrap()

        return self

    async def download_async(self) -> Self:
        if self._id is None:
            raise MECBlobException("No data to download")

        if self._data is not None:
            raise MECBlobException("This object already contains data")

        result = await data_api.get_data_async(self._server_url, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to download data")

        self._data = result.unwrap()

        return self
