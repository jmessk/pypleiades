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
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.INFO)

        if httpx_config:
            self._client = httpx.Client(**httpx_config)
            self._client_async = httpx.AsyncClient(**httpx_config)
        else:
            self._client = httpx.Client()
            self._client_async = httpx.AsyncClient()
