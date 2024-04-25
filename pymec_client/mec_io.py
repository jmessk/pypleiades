from enum import Enum, auto
import requests
import logging

from .mec_api import MECAPI, MECContentType


class MECIOException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECResStatus(Enum):
    OK = auto()
    FAILED = auto()


class MECIO(object):
    def __init__(self, server_url: str):
        self._server_url = server_url
        self._api = MECAPI(server_url)

    def get_data(self, data_id: str) -> str:
        (content_type, data) = self._api.get_data(data_id)

        if content_type == MECContentType.JSON:
            logging.error(data)
            raise MECIOException("Failed to fetch data.")

        logging.info("Data fetched.")

        return data

    def post_data(self, data: str, filename: str = "input") -> str:
        response_json = self._api.post_data(data, filename)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECIOException("Failed to upload data.")

        logging.info("Data uploaded.")

        return response_json["id"]
