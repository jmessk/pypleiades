from enum import Enum, auto
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]:[%(funcName)s()]: %(message)s",
)


class MECClientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECResStatus(Enum):
    OK = auto()
    FAILED = auto()


class MECClinet(object):
    def __init__(self, server_url: str):
        self._server_url = server_url

    def get_data(self, data_id: str) -> str:
        endpoint = f"{self._server_url}/data/{data_id}/blob"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        logging.debug("Data fetched.")

        # blob が json の場合は成功したのか判定できない
        # header から判定する？
        return response.text

    def post_data(self, data: str, filename: str = "input") -> dict[str, str]:
        endpoint = f"{self._server_url}/data"
        headers = {"Accept": "application/json"}

        file = {"file": (filename, data)}

        response = requests.post(
            endpoint,
            headers=headers,
            files=file,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to upload data.")

        logging.debug(response_json)

        return response_json

    def get_data_metadata(self, data_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/data/{data_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        response_json = response.json()

        if response_json["status"] != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to get data metadata.")

        logging.debug(response_json)

        return response_json

    def create_lambda(self, lambda_id: str, runtime: str) -> str:
        endpoint = f"{self._server_url}/lambda"
        headers = {"Accept": "application/json"}

        body_json = {
            "code_id": lambda_id,
            "runtime": runtime,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to create lambda.")

        logging.info("Lambda created.")
        logging.debug(response_json)

        return response_json["id"]

    def get_lambda_metadata(self, lambda_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/lambda/{lambda_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        response_json = response.json()

        if response_json["status"] != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to get lambda metadata.")

        logging.debug(response_json)

        return response_json

    def create_job(
        self,
        lambda_id: str,
        input_data_id: str,
        extra_tag: list[str],
    ) -> dict[str, str]:
        endpoint = f"{self._server_url}/job"
        headers = {"Accept": "application/json"}

        body_json = {
            "input_id": input_data_id,
            "functio": lambda_id,
            "extra_tag": extra_tag,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to create job.")

        logging.info("Job created.")
        logging.debug(response_json)

        return response_json

    def get_job_metadata(self, job_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/job/{job_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        response_json = response.json()

        if response_json["status"] != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to get job metadata.")

        logging.debug(response_json)

        return response_json

    def update_job_metadata(
        self,
        job_id: str,
        output_data_id: str,
        status: str,
    ):
        endpoint = f"{self._server_url}/job/{job_id}"
        headers = {"Accept": "application/json"}

        body_json = {
            "output": output_data_id,
            "status": status,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECClientException("Failed to update job metadata.")

        logging.info("Job metadata updated.")
        logging.debug(response_json)

    def register_worker():
        pass

    def get_worker_metadata() -> dict[str, str]:
        pass

    def contract_job():
        pass
