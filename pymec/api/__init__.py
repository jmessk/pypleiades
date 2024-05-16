import httpx
import logging
from typing import Optional


class MECAPI(object):
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
            self._logger: logging.Logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.INFO)

        self._client: httpx.Client = httpx.Client(**httpx_config)
        self._client_async: httpx.AsyncClient = httpx.AsyncClient(**httpx_config)

# User-Agent: pymec/v0.5.1
