# import swagger_client
from mec_io import MECIO
from mec_job import MECJob

import requests


class MECWorkerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECWorker(MECIO):
    # def __init__(self, client: swagger_client.ApiClient, runtimes: list[str]):
    #     super().__init__(client)

    #     self._worker_api = swagger_client.WorkerApi(client)
    #     self._job_api = swagger_client.JobApi(client)

    #     # Temporary client until API is updated
    #     self._connection = http.client.HTTPSConnection("mecrm.dolylab.cc")

    #     # Register worker when initialized
    #     self._worker_id = self._register(runtimes)

    def __init__(self, server_url: str, runtimes: list[str]):
        super().__init__(server_url)
        self._worker_id = self._register(runtimes)

    def _register(self, runtimes: list[str]) -> str:
        # request = swagger_client.RequestWorkerRegist(runtimes=runtimes)

        # print(request)

        # response: swagger_client.ResponseWorkerRegist = (
        #     self._worker_api.pleiades_worker_regist(body=request)
        # )

        # headers = {"Accept": "application/json"}

        # body = {
        #     "execulator": runtimes,
        # }

        # self._connection.request(
        #     "POST",
        #     "/api/v0.5/worker",
        #     headers=headers,
        #     body=json.dumps(body),
        # )

        # response = self._connection.getresponse()

        # data = response.read().decode("utf-8")
        # response_json: dict[str, str] = json.loads(data)

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

        if response_json["status"] != "ok":
            raise MECWorkerException("Failed to register worker.")

        return response_json["wid"]

    def contract(self, timeout: int = 20) -> MECJob | None:
        # request = swagger_client.RequestWorkerContract(
        #     worker_id=self._worker_id, timeout=5
        # )

        # response: swagger_client.ResponseWorkerContract = (
        #     self._worker_api.pleiades_worker_contract(
        #         w_id=self._worker_id, body=request
        #     )
        # )

        # headers = {"Accept": "application/json"}

        # body = {
        #     "extra_tag": [],
        #     "worker_id": self._worker_id,
        #     "timeout": 10,
        # }

        # self._connection.request(
        #     "POST",
        #     f"/api/v0.5/worker/{self._worker_id}/contract",
        #     headers=headers,
        #     body=json.dumps(body),
        # )

        # response = self._connection.getresponse()

        # data = response.read().decode("utf-8")
        # response_json: dict[str, str] = json.loads(data)

        endpoint = f"{self._server_url}/worker/{self._worker_id}/contract"
        headers = {"Accept": "application/json"}

        body_json = {
            "extra_tag": [],
            "worker_id": self._worker_id,
            "timeout": timeout,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("job_id"):
            return MECJob(self._server_url, response_json["job_id"])

        print(response_json)
        return None

    def get_info(self) -> dict[str, str]:
        endpoint = f"{self._server_url}/worker/{self._worker_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        return response.json()
