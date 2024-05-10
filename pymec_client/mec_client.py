from typing import Optional
import logging

from .mec_blob import MECBlob
from .mec_lambda import MECLambda
from .mec_worker import MECWorker


class MECClient(object):
    def __init__(
        self,
        server_url: str,
        logger: Optional[logging.Logger] = None,
    ):
        self._server_url = server_url
        self._logger = logger

    def new_blob(self) -> MECBlob:
        return MECBlob(self._server_url, logger=self._logger)
    
    def new_lambda(self) -> MECLambda:
        return MECLambda(self._server_url, logger=self._logger)
    
    def new_worker(self) -> MECWorker:
        return MECWorker(self._server_url, logger=self._logger)