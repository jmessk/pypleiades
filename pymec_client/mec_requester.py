import requests
import logging

from .mec_io import MECIO
from .mec_job import MECJob


class MECRequesterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECRequester(MECIO):
    def __init__(self, server_url: str):
        super().__init__(server_url)

    def create_lambda(self, lambda_id: str, runtime: str) -> str:
        # endpoint = f"{self._server_url}/lambda"
        # headers = {"Accept": "application/json"}

        # body_json = {
        #     "code_id": lambda_id,
        #     "runtime": runtime,
        # }

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        # response_json: dict[str, str] = response.json()

        # if response_json.get("status") != "ok":
        #     logging.error(response_json)
        #     raise MECRequesterException("Failed to create lambda.")

        # logging.info("Lambda created.")

        # return response_json["id"]

        response_json = self._api.create_lambda(lambda_id, runtime)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECRequesterException("Failed to create lambda.")

        logging.info("Lambda created.")

        return response_json["id"]

    def create_job(
        self,
        lambda_id: str,
        input_data_id: str,
        extra_tag: list = [],
    ) -> MECJob:
        # endpoint = f"{self._server_url}/job"
        # headers = {"Accept": "application/json"}

        # body_json = {
        #     "input_id": input_data_id,
        #     "functio": lambda_id,
        #     "extra_tag": [],
        # }

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        # response_json: dict[str, str] = response.json()

        # if response_json.get("status") != "ok":
        #     logging.error(response_json)
        #     raise MECRequesterException("Failed to create job.")

        # logging.info("Job created.")

        # return MECJob(self._server_url, response_json["jid"])

        response_json = self._api.create_job(lambda_id, input_data_id, extra_tag)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECRequesterException("Failed to create job.")

        logging.info("Job created.")

        return MECJob(self._server_url, response_json["jid"])
