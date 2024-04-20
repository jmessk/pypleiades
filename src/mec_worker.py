import swagger_client
from mec_io import MECIO
from mec_job import MECJob

import http.client
import json


class MECWorkerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECWorker(MECIO):
    def __init__(self, client: swagger_client.ApiClient, runtimes: list[str]):
        super().__init__(client)

        self._worker_api = swagger_client.WorkerApi(client)
        self._job_api = swagger_client.JobApi(client)

        # Temporary client until API is updated
        self._connection = http.client.HTTPSConnection("mecrm.dolylab.cc")

        # Register worker when initialized
        self._worker_id = self._register(runtimes)

    def get_info(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}

        self._connection.request(
            "GET",
            f"/api/v0.5/worker/{self._worker_id}",
            headers=headers,
        )

        response = self._connection.getresponse()
        data = response.read().decode("utf-8")

        return json.loads(data)

    def _register(self, runtimes: list[str]) -> str:
        # request = swagger_client.RequestWorkerRegist(runtimes=runtimes)

        # print(request)

        # response: swagger_client.ResponseWorkerRegist = (
        #     self._worker_api.pleiades_worker_regist(body=request)
        # )

        headers = {"Accept": "application/json"}

        body = {
            "execulator": runtimes,
        }

        self._connection.request(
            "POST",
            "/api/v0.5/worker",
            headers=headers,
            body=json.dumps(body),
        )

        response = self._connection.getresponse()

        data = response.read().decode("utf-8")
        response = json.loads(data)

        if response["wid"] is None:
            raise MECWorkerException("Failed to register worker.")

        return response["wid"]

    def contract(self) -> MECJob | None:
        # request = swagger_client.RequestWorkerContract(
        #     worker_id=self._worker_id, timeout=5
        # )

        # response: swagger_client.ResponseWorkerContract = (
        #     self._worker_api.pleiades_worker_contract(
        #         w_id=self._worker_id, body=request
        #     )
        # )

        headers = {"Accept": "application/json"}

        body = {
            "extra_tag": [],
            "worker_id": self._worker_id,
            "timeout": 10,
        }

        self._connection.request(
            "POST",
            f"/api/v0.5/worker/{self._worker_id}/contract",
            headers=headers,
            body=json.dumps(body),
        )

        response = self._connection.getresponse()

        data = response.read().decode("utf-8")
        response = json.loads(data)

        print(response)

        if response.get("job_id"):
            print("job created")
            return MECJob(self._client, response["job_id"])

        return None
