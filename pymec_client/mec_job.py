import requests
from enum import Enum, auto
from typing import Optional
import logging

from .mec_io import MECIO


class MECJobStatus(Enum):
    PREASSIGNED = auto()
    ENQUEUED = auto()
    RUNNING = auto()
    FINISHED = auto()
    ERROR = auto()


class MECJobException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECJob(MECIO):
    def __init__(self, server_url: str, job_id: str):
        super().__init__(server_url)
        self._job_id = job_id

        self._output_data_id: Optional[str] = None

    def get_info(self) -> dict[str, str]:
        endpoint = f"{self._server_url}/job/{self._job_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        return response.json()

    def get_lambda_and_input_data(self) -> tuple[str, str]:
        response = self.get_info()

        input_lambda = self.get_data(response["lambda_id"])
        input_data = self.get_data(response["job_input_id"])

        return (input_lambda, input_data)

    def finish(self, data: str):
        output_data_id = self.post_data(data, "output.txt")

        endpoint = f"{self._server_url}/job/{self._job_id}"
        headers = {"Accept": "application/json"}

        body_json = {
            "output": output_data_id,
            "status": "finished",
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECJobException("Failed to finish job.")
        
        logging.info("Job finished.")

    def is_finished(self) -> bool:
        """Check if the job is finished.

        Q: Why do you use the property `self._output_data_id` ?
        A: To avoid sending unnecessary requests in get_output_data().
           In the point when `job_status` becomes `Finished`, `output_data_id` is available.
        """
        response = self.get_info()

        if response["job_status"] == "Finished":
            logging.info("Job finished.")
            self._output_data_id = response["job_output_id"]
            return True

        logging.debug("job_status: %s", response["job_status"])

        return False

    def get_output_data(self) -> str:
        if self._output_data_id is None:
            raise MECJobException("Output data is not available.")

        return self.get_data(self._output_data_id)
