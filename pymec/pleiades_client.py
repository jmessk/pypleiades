from typing import Optional
import logging

from .mec_blob import MECBlob
from .mec_lambda import MECLambda
from .mec_job import MECJob
from .mec_worker import MECWorker


class PleiadesClient(object):
    __slots__ = ["_server_url", "_logger", "_httpx_config"]

    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
        httpx_config: Optional[dict] = None,
    ):
        self._server_url = server_url
        self._logger = logger
        self._httpx_config = httpx_config

    def new_blob(self) -> MECBlob:
        return MECBlob(
            self._server_url, logger=self._logger, httpx_config=self._httpx_config
        )

    def new_lambda(self) -> MECLambda:
        return MECLambda(
            self._server_url, logger=self._logger, httpx_config=self._httpx_config
        )

    def new_job(self) -> MECJob:
        return MECJob(
            self._server_url, logger=self._logger, httpx_config=self._httpx_config
        )

    def new_worker(self) -> MECWorker:
        return MECWorker(
            self._server_url, logger=self._logger, httpx_config=self._httpx_config
        )
