from typing import Optional
import logging

from .mec_io import MECIO, AsyncMECIO


class MECJobException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECJob(MECIO):
    def __init__(self, server_url: str, job_id: str):
        super().__init__(server_url)
        self._job_id = job_id
        self._output_data_id: Optional[str] = None

        job_metadata = self.get_info()

        self._lambda_data_id = job_metadata["lambda_id"]
        self._input_data_id = job_metadata["job_input_id"]

    def get_info(self) -> dict[str, str]:
        response_json = self._api.get_job_metadata(self._job_id)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECJobException("Failed to fetch job metadata.")

        logging.info("Job metadata fetched.")

        return response_json

    def get_lambda_data(self) -> bytes:
        return self.get_data(self._lambda_data_id)

    def get_input_data(self) -> bytes:
        return self.get_data(self._input_data_id)

    def get_lambda_and_input_data(self) -> tuple[bytes, bytes]:
        return (
            self.get_lambda_data(),
            self.get_input_data(),
        )

    def finish(self, data: str):
        output_data_id = self.post_data(data)
        response_json = self._api.update_job_metadata(
            self._job_id, output_data_id, "finished"
        )

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECJobException("Failed to finish job.")

        logging.info("Job finished.")

    def is_finished(self) -> bool:
        response_json = self.get_info()

        if response_json["job_status"] == "Finished":
            logging.info("Job finished.")

            # Q: Why do you use the property `self._output_data_id` ?
            # A: To avoid sending unnecessary requests in get_output_data().
            #    In the point when `job_status` becomes `Finished`, `output_data_id` is available.
            self._output_data_id = response_json["job_output_id"]

            return True

        logging.info("job_status: %s", response_json["job_status"])

        return False

    def get_output_data(self) -> bytes:
        if self._output_data_id is None:
            raise MECJobException("Output data is not available.")

        return self.get_data(self._output_data_id)


class AsyncMECJob(AsyncMECIO):
    def __init__(self, server_url: str, job_id: str, httpx_config: dict = {}):
        super().__init__(server_url, httpx_config=httpx_config)
        self._job_id = job_id
        self._output_data_id: Optional[str] = None

    async def async_init(self):
        job_metadata = await self.get_info()

        self._lambda_data_id = job_metadata["lambda_id"]
        self._input_data_id = job_metadata["job_input_id"]

        return self

    async def get_info(self) -> dict[str, str]:
        response_json = await self._api.get_job_metadata(self._job_id)

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECJobException("Failed to fetch job metadata.")

        logging.info("Job metadata fetched.")

        return response_json

    async def get_lambda_data(self) -> bytes:
        return await self.get_data(self._lambda_data_id)

    async def get_input_data(self) -> bytes:
        return await self.get_data(self._input_data_id)

    async def get_lambda_and_input_data(self) -> tuple[bytes, bytes]:
        return (
            await self.get_lambda_data(),
            await self.get_input_data(),
        )

    async def finish(self, data: str):
        output_data_id = await self.post_data(data)
        response_json = await self._api.update_job_metadata(
            self._job_id, output_data_id, "finished"
        )

        if response_json.get("status") != "ok":
            logging.error(response_json)
            raise MECJobException("Failed to finish job.")

        logging.info("Job finished.")

    async def is_finished(self) -> bool:
        response_json = await self.get_info()

        if response_json["job_status"] == "Finished":
            logging.info("Job finished.")

            # Q: Why do you use the property `self._output_data_id` ?
            # A: To avoid sending unnecessary requests in get_output_data().
            #    In the point when `job_status` becomes `Finished`, `output_data_id` is available.
            self._output_data_id = response_json["job_output_id"]

            return True

        logging.info("job_status: %s", response_json["job_status"])

        return False

    async def get_output_data(self) -> bytes:
        if self._output_data_id is None:
            raise MECJobException("Output data is not available.")

        return await self.get_data(self._output_data_id)
