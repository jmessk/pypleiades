import logging

from .pleiades_api import MECAPI, AsyncMECAPI, MECContentType


class MECIOException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECIO(object):
    def __init__(self, server_url: str):
        self._server_url = server_url
        self._api = MECAPI(server_url)

    def get_data(self, data_id: str) -> bytes:
        (content_type, data) = self._api.get_data(data_id)

        if content_type == MECContentType.JSON:
            logging.error(data)
            raise MECIOException("Failed to fetch data.")

        logging.info("Data fetched.")

        return data

    def post_data(self, data: bytes, filename: str = "input") -> str:
        response_json = self._api.post_data(data, filename)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECIOException("Failed to upload data.")

        logging.info("Data uploaded.")

        return response_json["id"]


class AsyncMECIO(object):
    def __init__(self, server_url: str, httpx_config: dict = {}):
        self._server_url = server_url
        self._api = AsyncMECAPI(server_url, httpx_config=httpx_config)

    async def get_data(self, data_id: str) -> bytes:
        (content_type, data) = await self._api.get_data(data_id)

        if content_type == MECContentType.JSON:
            logging.error(data)
            raise MECIOException("Failed to fetch data.")

        logging.info("Data fetched.")

        return data

    async def post_data(self, data: bytes, filename: str = "input") -> str:
        response_json = await self._api.post_data(data, filename)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECIOException("Failed to upload data.")

        logging.info("Data uploaded.")

        return response_json["id"]
