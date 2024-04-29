from enum import Enum, auto
import requests
import httpx
import logging
from io import BytesIO


class MECContentType(Enum):
    JSON = auto()
    BLOB = auto()


class MECAPI(object):
    def __init__(self, server_url: str):
        self._server_url = server_url

    def get_data(self, data_id: str) -> tuple[MECContentType, bytes | dict[str, str]]:
        endpoint = f"{self._server_url}/data/{data_id}/blob"
        headers = {"Accept": "application/octet-stream"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        # If the response is JSON, return the JSON object
        # `response.headers` returns a `CaseInsensitiveDict`
        if response.headers.get("content-type") == "application/json":
            response_json: dict[str, str] = response.json()
            logging.debug(response_json)

            return (MECContentType.JSON, response_json)

        logging.debug("content-type: application/octet-stream")

        return (MECContentType.BLOB, response.content)

    def post_data(self, data: bytes, filename: str = "input") -> dict[str, str]:
        endpoint = f"{self._server_url}/data"
        headers = {"Accept": "application/json"}

        # file = {"file": (filename, data)}
        file = {"file": (filename, BytesIO(data))}

        response = requests.post(
            endpoint,
            headers=headers,
            files=file,
        )

        response_json: dict[str, str] = response.json()
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
        logging.debug(response_json)

        return response_json

    def create_lambda(self, lambda_data_id: str, runtime: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/lambda"
        headers = {"Accept": "application/json"}

        body_json = {
            "code_id": lambda_data_id,
            "runtime": runtime,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    def get_lambda_metadata(self, lambda_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/lambda/{lambda_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        response_json = response.json()

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

        logging.debug(response_json)

        return response_json

    def update_job_metadata(
        self,
        job_id: str,
        output_data_id: str,
        status: str,
    ) -> dict[str, str]:
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

        logging.debug(response_json)

        return response_json

    def register_worker(self, runtimes: list[str]) -> dict[str, str]:
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

        logging.debug(response_json)

        return response_json

    def get_worker_metadata(self, worker_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/worker/{worker_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    def contract_job(
        self,
        worker_id: str,
        extra_tag: list[str],
        timeout: int,
    ) -> dict[str, str]:
        endpoint = f"{self._server_url}/worker/{worker_id}/contract"
        headers = {"Accept": "application/json"}

        body_json = {
            "extra_tag": extra_tag,
            "worker_id": worker_id,
            "timeout": timeout,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json


class AsyncMECAPI(object):
    def __init__(self, server_url: str, httpx_config: dict = {}):
        self._server_url = server_url
        self._config = httpx_config

    async def get_data(
        self, data_id: str
    ) -> tuple[MECContentType, bytes | dict[str, str]]:
        endpoint = f"{self._server_url}/data/{data_id}/blob"
        headers = {"Accept": "application/octet-stream"}

        # response = requests.get(
        #     endpoint,
        #     headers=headers,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.get(
                endpoint,
                headers=headers,
            )

        # If the response is JSON, return the JSON object
        # `response.headers` returns a `CaseInsensitiveDict`
        if response.headers.get("content-type") == "application/json":
            response_json: dict[str, str] = response.json()
            logging.debug(response_json)

            return (MECContentType.JSON, response_json)

        logging.debug("content-type: application/octet-stream")

        return (MECContentType.BLOB, response.content)

    async def post_data(self, data: bytes, filename: str = "input") -> dict[str, str]:
        endpoint = f"{self._server_url}/data"
        headers = {"Accept": "application/json"}

        # file = {"file": (filename, data)}
        file = {"file": (filename, BytesIO(data))}

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     files=file,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                files=file,
            )

        response_json: dict[str, str] = response.json()
        logging.debug(response_json)

        return response_json

    async def get_data_metadata(self, data_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/data/{data_id}"
        headers = {"Accept": "application/json"}

        # response = requests.get(
        #     endpoint,
        #     headers=headers,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.get(
                endpoint,
                headers=headers,
            )

        response_json = response.json()
        logging.debug(response_json)

        return response_json

    async def create_lambda(self, lambda_data_id: str, runtime: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/lambda"
        headers = {"Accept": "application/json"}

        body_json = {
            "code_id": lambda_data_id,
            "runtime": runtime,
        }

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=body_json,
            )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    async def get_lambda_metadata(self, lambda_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/lambda/{lambda_id}"
        headers = {"Accept": "application/json"}

        # response = requests.get(
        #     endpoint,
        #     headers=headers,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.get(
                endpoint,
                headers=headers,
            )

        response_json = response.json()

        logging.debug(response_json)

        return response_json

    async def create_job(
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

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=body_json,
            )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    async def get_job_metadata(self, job_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/job/{job_id}"
        headers = {"Accept": "application/json"}

        # response = requests.get(
        #     endpoint,
        #     headers=headers,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.get(
                endpoint,
                headers=headers,
            )

        response_json = response.json()

        logging.debug(response_json)

        return response_json

    async def update_job_metadata(
        self,
        job_id: str,
        output_data_id: str,
        status: str,
    ) -> dict[str, str]:
        endpoint = f"{self._server_url}/job/{job_id}"
        headers = {"Accept": "application/json"}

        body_json = {
            "output": output_data_id,
            "status": status,
        }

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=body_json,
            )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    async def register_worker(self, runtimes: list[str]) -> dict[str, str]:
        endpoint = f"{self._server_url}/worker"
        headers = {"Accept": "application/json"}

        body_json = {
            "execulator": runtimes,
        }

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=body_json,
            )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    async def get_worker_metadata(self, worker_id: str) -> dict[str, str]:
        endpoint = f"{self._server_url}/worker/{worker_id}"
        headers = {"Accept": "application/json"}

        # response = requests.get(
        #     endpoint,
        #     headers=headers,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.get(
                endpoint,
                headers=headers,
            )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json

    async def contract_job(
        self,
        worker_id: str,
        extra_tag: list[str],
        timeout: int,
    ) -> dict[str, str]:
        endpoint = f"{self._server_url}/worker/{worker_id}/contract"
        headers = {"Accept": "application/json"}

        body_json = {
            "extra_tag": extra_tag,
            "worker_id": worker_id,
            "timeout": timeout,
        }

        # response = requests.post(
        #     endpoint,
        #     headers=headers,
        #     json=body_json,
        # )

        async with httpx.AsyncClient(**self._config) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=body_json,
            )

        response_json: dict[str, str] = response.json()

        logging.debug(response_json)

        return response_json
