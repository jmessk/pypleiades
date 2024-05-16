from typing import Optional, Any
import logging


class MECObject(object):
    __slots__ = [
        "_server_url",
        "_id",
        "_logger",
        "_httpx_config",
    ]

    def __init__(
        self,
        server_url: str,
        id: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        self._server_url = server_url
        self._id = id

        if logger:
            self._logger: logging.Logger = logger
        else:
            self._logger = logging.getLogger()
            self._logger.setLevel(logging.INFO)

        if httpx_config:
            self._httpx_config = httpx_config
        else:
            self._httpx_config = {
                "timeout": 30.0,
            }

    @property
    def id(self) -> str:
        if self._id is None:
            raise ValueError("id is not set")
        return self._id

    def remote_info(self) -> Any:
        raise NotImplementedError()

    async def remote_info_async(self) -> Any:
        raise NotImplementedError()

    def has_remote(self) -> bool:
        return self._id is not None
