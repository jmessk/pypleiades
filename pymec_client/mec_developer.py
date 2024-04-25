import requests
import logging

from .mec_io import MECIO


class MECDeveloperException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECDeveloper(MECIO):
    def __init__(self, server_url: str):
        super().__init__(server_url)

    def create_lambda(self, lambda_id: str, runtime: str) -> str:
        response_json = self._api.create_lambda(lambda_id, runtime)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECDeveloperException("Failed to create lambda.")

        logging.info("Lambda created.")

        return response_json["id"]
