from typing import Optional
from typing_extensions import Self
import logging

from .api import kv_api
from .mec_object import MECObject


class MECKVNamespace(MECObject):
    __slots__ = [
        # super
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
        # self
        "_kv_api",
        "_consistency",
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

        self._kv_api = kv_api.KVAPI(
            self._server_url,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )

        self._consistency: kv_api.KVConsistency = kv_api.KVConsistency.NONE

    # set namespace id

    def set_namespace_id(self, namespace_id: str) -> Self:
        if self.has_remote():
            raise Exception("Remote already exists")

        self._id = namespace_id
        self._logger.info(f"Set namespace id to {namespace_id}")

        return self

    # consistency

    def set_consistency(self, consistency: kv_api.KVConsistency) -> Self:
        self._consistency = consistency
        self._logger.info(f"Set consistency to {consistency.value}")

        return self

    # create

    def create(self) -> Self:
        if self.has_remote():
            raise Exception("Remote already exists")

        result = self._kv_api.create_namespace(consistency=self._consistency)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception("Failed to create namespace")

        self._id = result.unwrap().namespace_id
        self._logger.info(f"Created namespace {self._id} .")

        return self

    async def create_async(self) -> Self:
        if self.has_remote():
            raise Exception("Remote already exists")

        result = await self._kv_api.create_namespace_async(
            consistency=self._consistency
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception("Failed to create namespace")

        self._id = result.unwrap().namespace_id
        self._logger.info(f"Created namespace {self._id} .")

        return self

    # handler

    def new_key(self, key: str) -> "KVHandler":
        if not self.has_remote():
            raise Exception("Remote does not exist")

        return KVHandler(
            self._id,
            self._kv_api,
            self._server_url,
            id=key,
            logger=self._logger,
            httpx_config=self._httpx_config,
        )


class KVHandler(MECObject):
    __slots__ = [
        # super
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
        # self
        "_namespace_id",
        "_kv_api",
    ]

    def __init__(
        self,
        namespace_id: str,
        kv_api: kv_api.KVAPI,
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

        self._namespace_id = namespace_id
        self._kv_api = kv_api

    # check

    def has_namespace(self) -> bool:
        return self._namespace_id is not None

    # set

    def set(
        self,
        value: str,
        expire: int = 0,
        get: bool = False,
        append: bool = False,
    ):
        if not self.has_namespace():
            raise Exception("Namespace does not exist")

        if not self.has_remote():
            raise Exception("Remote does not exist")

        result = self._kv_api.set_value(
            self._namespace_id,
            self._id,
            value=value,
            expire=expire,
            get=get,
            append=append,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception("Failed to set")

        self._logger.info(f"Set value to `{self._id}`.")

        return self

    async def set_async(
        self,
        value: str,
        expire: int = 0,
        get: bool = False,
        append: bool = False,
    ):
        if not self.has_namespace():
            raise Exception("Namespace does not exist")

        if not self.has_remote():
            raise Exception("Remote does not exist")

        result = await self._kv_api.set_value_async(
            self._namespace_id,
            self._id,
            value=value,
            expire=expire,
            get=get,
            append=append,
        )

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception("Failed to set")

        self._logger.info(f"Set value to `{self._id}`.")

        return self

    # get

    def get(self) -> str:
        if not self.has_namespace():
            raise Exception("Namespace does not exist")

        if not self.has_remote():
            raise Exception("Remote does not exist")

        result = self._kv_api.get_value(self._namespace_id, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception("Failed to get")

        self._logger.info(f"Get value from `{self._id}`.")

        return result.unwrap().value

    async def get_async(self) -> str:
        if not self.has_namespace():
            raise Exception("Namespace does not exist")

        if not self.has_remote():
            raise Exception("Remote does not exist")

        result = await self._kv_api.get_value_async(self._namespace_id, self._id)

        if result.is_err():
            self._logger.error(result.unwrap_err())
            raise Exception("Failed to get")

        self._logger.info(f"Get value from `{self._id}`.")

        return result.unwrap().value
