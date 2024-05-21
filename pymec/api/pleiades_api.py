import httpx
import logging
from typing import Optional



class PleiadesAPI(object):
    __slots__ = ["_server_url", "_logger", "_client", "_client_async"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        self._server_url = server_url

        if logger:
            self._logger: logging.Logger = logger
        else:
            logger = logging.getLogger("pleiades")
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter(
                        "%(asctime)s - %(module)s::%(funcName)s - [%(levelname)s] - %(message)s"
                )
                handler.setFormatter(formatter)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(handler)
                logger.propagate = False
            self._logger = logger

        self._client: httpx.Client = httpx.Client(**httpx_config)
        self._client_async: httpx.AsyncClient = httpx.AsyncClient(**httpx_config)


# User-Agent: pymec/v0.5.1
