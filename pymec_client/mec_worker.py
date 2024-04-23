import requests
from typing import Optional
import logging

from .mec_io import MECIO
from .mec_job import MECJob


# MEC Worker
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
        endpoint = f"{self._server_url}/worker"
        headers = {"Accept": "application/json"}

        body_json = {
            "execulator": runtimes,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json["status"] != "ok":
            logging.error(response_json)
            raise MECWorkerException("Failed to register worker.")

        logging.info("Worker registered.")
        logging.debug(response_json)

        self._worker_id = response_json["wid"]

    def contract(self, extra_tag: list[str] = [], timeout: int = 20) -> Optional[MECJob]:
        if self._worker_id is None:
            raise MECWorkerException("Worker is not registered.")
        
        logging.info("Contracting job...")

        endpoint = f"{self._server_url}/worker/{self._worker_id}/contract"
        headers = {"Accept": "application/json"}

        body_json = {
            "extra_tag": extra_tag,
            "worker_id": self._worker_id,
            "timeout": timeout,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("job_id"):
            logging.info("Job contracted.")
            return MECJob(self._server_url, response_json["job_id"])

        logging.info("No job.")
        logging.debug(response_json)
        
        return None

    def get_info(self) -> dict[str, str]:
        if self._worker_id is None:
            raise MECWorkerException("Worker is not registered.")

        endpoint = f"{self._server_url}/worker/{self._worker_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        return response.json()
