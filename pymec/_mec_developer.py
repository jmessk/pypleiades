import logging

from .mec_io import MECIO, AsyncMECIO


class MECDeveloperException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECDeveloper(MECIO):
    def __init__(self, server_url: str):
        super().__init__(server_url)

    def create_lambda_by_id(self, lambda_data_id: str, runtime: str) -> str:
        response_json = self._api.create_lambda(lambda_data_id, runtime)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECDeveloperException("Failed to create lambda.")

        logging.info("Lambda created.")

        return response_json["id"]
    
    def create_lambda_by_bytes(self, lambda_data_bytes: bytes, runtime: str) -> str:
        lambda_data_id = self.post_data(lambda_data_bytes)

        response_json = self._api.create_lambda(lambda_data_id, runtime)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECDeveloperException("Failed to create lambda.")

        logging.info("Lambda created.")

        return response_json["id"]


class AsyncMECDeveloper(AsyncMECIO):
    def __init__(self, server_url: str, httpx_config: dict = {}):
        super().__init__(server_url, httpx_config=httpx_config)

    async def create_lambda_by_id(self, lambda_data_id: str, runtime: str) -> str:
        response_json = await self._api.create_lambda(lambda_data_id, runtime)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECDeveloperException("Failed to create lambda.")

        logging.info("Lambda created.")

        return response_json["id"]

    async def create_lambda_by_bytes(self, lambda_data_bytes: bytes, runtime: str) -> str:
        lambda_data_id = await self.post_data(lambda_data_bytes)

        response_json = await self._api.create_lambda(lambda_data_id, runtime)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECDeveloperException("Failed to create lambda.")

        logging.info("Lambda created.")

        return response_json["id"]
