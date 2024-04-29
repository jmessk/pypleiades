from typing import Optional
import logging

from .mec_io import MECIO, AsyncMECIO
from .mec_job import MECJob, AsyncMECJob


class MECWorkerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECWorker(MECIO):
    def __init__(
        self,
        server_url: str,
    ):
        super().__init__(server_url)
        self._worker_id: Optional[str] = None

    def register(self, runtimes: list[str]):
        response_json = self._api.register_worker(runtimes)

        if response_json["status"] != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to register worker.")

        logging.info("Worker registered.")

        self._worker_id = response_json["wid"]

    def contract(
        self,
        extra_tag: list[str] = [],
        timeout: int = 20,
    ) -> Optional[MECJob]:
        if self._worker_id is None:
            raise MECWorkerException("Worker is not registered.")

        logging.info("Contracting job...")

        response_json = self._api.contract_job(self._worker_id, extra_tag, timeout)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to contract job.")

        elif response_json.get("job_id"):
            logging.info("Job contracted.")
            return MECJob(self._server_url, response_json["job_id"])

        logging.info("No job.")

        return None

    def get_info(self) -> dict[str, str]:
        if self._worker_id is None:
            raise MECWorkerException("Worker is not registered.")

        response_json = self._api.get_worker_metadata(self._worker_id)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to fetch worker metadata.")

        logging.info("Worker metadata fetched.")

        return response_json


class AsyncMECWorker(AsyncMECIO):
    def __init__(
        self,
        server_url: str,
    ):
        super().__init__(server_url)
        self._worker_id: Optional[str] = None

    async def register(self, runtimes: list[str]):
        response_json = await self._api.register_worker(runtimes)

        if response_json["status"] != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to register worker.")

        logging.info("Worker registered.")

        self._worker_id = response_json["wid"]

    async def contract(
        self,
        extra_tag: list[str] = [],
        timeout: int = 20,
    ) -> Optional[AsyncMECJob]:
        if self._worker_id is None:
            raise MECWorkerException("Worker is not registered.")

        logging.info("Contracting job...")

        response_json = await self._api.contract_job(self._worker_id, extra_tag, timeout)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to contract job.")

        elif response_json.get("job_id"):
            logging.info("Job contracted.")
            return await AsyncMECJob(self._server_url, response_json["job_id"]).async_init()

        logging.info("No job.")

        return None

    async def get_info(self) -> dict[str, str]:
        if self._worker_id is None:
            raise MECWorkerException("Worker is not registered.")

        response_json = await self._api.get_worker_metadata(self._worker_id)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to fetch worker metadata.")

        logging.info("Worker metadata fetched.")

        return response_json
