from typing import Optional, Any
import logging
import sys


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
            logger = logging.getLogger(__name__)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            self._logger = logger

        if httpx_config:
            self._httpx_config = httpx_config
        else:
            self._httpx_config = {
                "timeout": None,
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
