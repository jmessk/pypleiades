import swagger_client
from mec_io import MECIO, MECResStatus
from mec_job import MECJob


class MECWorkerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECWorker(MECIO):
    def __init__(self, client: swagger_client.ApiClient, runtimes: list[str]):
        super().__init__(client)
        self._worker_api = swagger_client.WorkerApi(client)
        self._job_api = swagger_client.JobApi(client)

        self._worker_id = self._register(runtimes)

    def _register(self, runtimes: list[str]) -> str:
        request = swagger_client.RequestWorkerRegist(runtimes=runtimes)

        response: swagger_client.ResponseWorkerRegist = (
            self._worker_api.pleiades_worker_regist(body=request)
        )

        print(response)

        match response.status:
            case "ok":
                return response.wid
            case _:
                raise MECWorkerException("Failed to register worker.")

    def contract(self) -> MECJob | None:
        request = swagger_client.RequestWorkerContract(
            worker_id=self._worker_id, timeout=5
        )

        response: swagger_client.ResponseWorkerContract = (
            self._worker_api.pleiades_worker_contract(
                w_id=self._worker_id, body=request
            )
        )

        print(response)

        if response.job_id is None:
            return None
        
        return MECJob(self._client, response.job_id)
