import logging

from .mec_io import MECIO, AsyncMECIO
from .mec_job import MECJob, AsyncMECJob


class MECRequesterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECRequester(MECIO):
    def __init__(self, server_url: str):
        super().__init__(server_url)

    def create_job_by_id(
        self,
        lambda_id: str,
        input_data_id: str,
        extra_tag: list = [],
    ) -> MECJob:
        """Create a job by lambda id and input data id.

        # Parameters

        - `lambda_id: str`
          lambda id not lambda blob data id
        - `input_data_id: str`
          blob data id to be used as input data
        - `extra_tag: list`
          extra tag

        # Attention

        - `lambda_id` should be obtained from the function implements the lambda endpoint.
        """

        response_json = self._api.create_job(lambda_id, input_data_id, extra_tag)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECRequesterException("Failed to create job.")

        logging.info("Job created.")

        return MECJob(self._server_url, response_json["jid"])

    def create_job_by_bytes(
        self,
        lambda_id: str,
        input_data_bytes: bytes,
        extra_tag: list = [],
    ) -> MECJob:
        input_data_id = self.post_data(input_data_bytes)

        response_json = self._api.create_job(lambda_id, input_data_id, extra_tag)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECRequesterException("Failed to create job.")

        logging.info("Job created.")

        return MECJob(self._server_url, response_json["jid"])


class AsyncMECRequester(AsyncMECIO):
    def __init__(self, server_url: str):
        super().__init__(server_url)

    async def create_job_by_id(
        self,
        lambda_id: str,
        input_data_id: str,
        extra_tag: list = [],
    ) -> AsyncMECJob:
        """Create a job by lambda id and input data id.

        # Parameters

        - `lambda_id: str`
          lambda id not lambda blob data id
        - `input_data_id: str`
          blob data id to be used as input data
        - `extra_tag: list`
          extra tag

        # Attention

        - `lambda_id` should be obtained from the function implements the lambda endpoint.
        """

        response_json = await self._api.create_job(lambda_id, input_data_id, extra_tag)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECRequesterException("Failed to create job.")

        logging.info("Job created.")

        return await AsyncMECJob(self._server_url, response_json["jid"]).async_init()

    async def create_job_by_bytes(
        self,
        lambda_id: str,
        input_data_bytes: bytes,
        extra_tag: list = [],
    ) -> AsyncMECJob:
        input_data_id = await self.post_data(input_data_bytes)

        response_json = await self._api.create_job(lambda_id, input_data_id, extra_tag)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECRequesterException("Failed to create job.")

        logging.info("Job created.")

        return await AsyncMECJob(self._server_url, response_json["jid"]).async_init()
