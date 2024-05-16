from typing import Optional
from typing_extensions import Self
import logging
import aiofiles

from .api import data_api
from .mec_object import MECObject


class MECBlobException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECBlob(MECObject):
    __slots__ = [
        # super
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
        # self
        "_data_api",
        "_data",
    ]

    def __init__(
        self,
        server_url: str,
        id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        """MECBlob

        Class for handling Blob.

        Args:
            server_url (str): Specify the MECRM URL to use
            id (Optional[str]): Data ID on MECRM
            logger (Optional[logging.Logger]): logging object

        """

        super().__init__(
            server_url=server_url,
            id=id,
            logger=logger,
            httpx_config=httpx_config,
        )

        self._data_api = data_api.DataAPI(
            self._server_url,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._data: Optional[bytes] = None

    # check

    def has_data(self) -> bool:
        return self._data is not None

    # data

    def get_data(self) -> bytes:
        # リモートに存在するがデータがない場合は取得する
        if self.has_remote() and not self.has_data():
            self.fetch()

        # リモートにもデータがなくローカルにもデータがない場合は例外を投げる
        if not self.has_data():
            raise MECBlobException("No data to get.")

        return self._data

    async def get_data_async(self) -> bytes:
        # リモートに存在するがデータがない場合は取得する
        if self.has_remote() and not self.has_data():
            await self.fetch_async()

        # リモートにもデータがなくローカルにもデータがない場合は例外を投げる
        if not self.has_data():
            raise MECBlobException("No data to get.")

        return self._data

    # info

    def remote_info(self) -> data_api.RespDataInfo:
        """remote_info

        Get blob metadata in remote MECRM.

        Args:
            None

        Returns:
            data_api.RespDataInfo

        Raises:
            Exception: If the remote object does not exist.

        """

        if not self.has_remote():
            raise MECBlobException("No data to get info.")

        result = self._data_api.info(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to get data info.")

        self._logger.info("Fetched remote Blob info.")

        return result.unwrap()

    async def remote_info_async(self) -> data_api.RespDataInfo:
        """remote_info_async

        Asyncronously get blob metadata in remote MECRM.

        Args:
            None

        Returns:
            data_apiDataInfo

        Raises:
            Exception: If the remote object does not exist.

        """

        if not self.has_remote():
            raise MECBlobException("No data to get info.")

        result = await self._data_api.info_async(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to get data info.")

        self._logger.info("Fetch remote Blob info.")

        return result.unwrap()

    # from bytes

    def from_bytes(self, data: bytes) -> Self:
        """from_file

        Set the Blob from bytes.

        Args:
            data (bytes): bytes object

        Returns:
            Self

        Raises:
            Exception: If object already contains Blob.

        """

        if self._data is not None:
            raise MECBlobException("Data already exists.")

        self._data = data
        self._logger.info("Set data bytes.")

        return self

    # from file

    def from_file(self, file_path: str) -> Self:
        """from_file

        Load and set the Blob from a local file.

        Args:
            file_path (str): File path to set.

        Returns:
            Self

        Raises:
            Exception: If object already contains Blob.

        """

        with open(file_path, "rb") as file:
            self.from_bytes(file.read())

        self._logger.info(f"Loaded data from {file_path} .")

        return self

    async def from_file_async(self, file_path: str) -> Self:
        """from_file_async

        Asyncronously load and set the Blob from a local file.

        Args:
            file_path (str): File path to load.

        Returns:
            Self

        Raises:
            Exception: If object already contains Blob.

        """

        async with aiofiles.open(file_path, "rb") as file:
            self.from_bytes(await file.read())

        self._logger.info(f"Loaded data from {file_path} .")

        return self

    # save as file

    def save(self, file_path: str) -> Self:
        """save

        Save blob as a local file
        """

        with open(file_path, "wb") as file:
            file.write(self._data)

        self._logger.info(f"Saved data to {file_path} .")

        return self

    async def save_async(self, file_path: str) -> Self:
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(self._data)

        self._logger.info(f"Saved data to {file_path} .")

        return self

    # upload

    def upload(self) -> Self:
        if self.has_remote():
            raise MECBlobException("Data already exists on remote server.")

        if not self.has_data():
            raise MECBlobException("No data to upload.")

        result = self._data_api.post_data(self._data)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to upload data.")

        self._id = result.unwrap().data_id
        self._logger.info(f"Uploaded data to {self._id} .")

        return self

    async def upload_async(self) -> Self:
        if self.has_remote():
            raise MECBlobException("Data already exists on remote server.")

        if not self.has_data():
            raise MECBlobException("No data to upload.")

        result = await self._data_api.post_data_async(self._data)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to upload data.")

        self._id = result.unwrap().data_id
        self._logger.info(f"Uploaded data to {self._id} .")

        return self

    # download
    # __init__ では async は使えないので、別途関数を用意する。
    # 自動的にダウンロードするのではなく、明示的にダウンロードするようにする。
    # そのほうがユーザが意図しないタイミングでのダウンロードを防げる。

    def fetch(self) -> Self:
        if self.has_data():
            raise MECBlobException("Data already fetched.")

        result = self._data_api.get_data(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to download data.")

        self._data = result.unwrap()
        self._logger.info(f"Fetched data from {self._id} .")

        return self

    async def fetch_async(self) -> Self:
        if self.has_data():
            raise MECBlobException("Data already fetched.")

        result = await self._data_api.get_data_async(self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise MECBlobException("Failed to download data.")

        self._data = result.unwrap()
        self._logger.info(f"Fetched data from {self._id} .")

        return self
