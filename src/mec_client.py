import swagger_client
from mec_io import MECIO, MECResStatus
from mec_job import MECJob


class MECClient(MECIO):
    def __init__(self, client: swagger_client.ApiClient):
        super().__init__(client)
        self._worker_api = swagger_client.WorkerApi(client)

    def register(self, runtimes: list[str]) -> tuple[MECResStatus, str]:
        request = swagger_client.RequestWorkerRegist(runtimes=runtimes)

        response: swagger_client.ResponseWorkerRegist = (
            self._worker_api.pleiades_worker_regist(body=request)
        )

        status = MECResStatus.OK if response.status == "ok" else MECResStatus.FAILED
        value = (
            response.wid if status == MECResStatus.OK else "Failed to register worker."
        )

        return (status, value)

    def contract(self, worker_id: str) -> tuple[MECResStatus, str]:
        request = swagger_client.RequestWorkerContract(worker_id=worker_id, timeout=20)

        response: swagger_client.ResponseWorkerContract = (
            self._worker_api.pleiades_worker_contract(body=request)
        )

        status = MECResStatus.OK if response.status == "ok" else MECResStatus.FAILED
        value = (
            response.job_id
            if status == MECResStatus.OK
            else "Failed to contract worker."
        )

        return (status, value)

    def create_job(self, input_id: str, lambda_id: str) -> tuple[MECResStatus, MECJob | str]:
        request = swagger_client.RequestJobCreate(
            input_id=input_id, lambda_id=lambda_id
        )

        response: swagger_client.ResponseJobCreate = self._job_api.pleiades_job_create(
            body=request
        )

        status = MECResStatus.OK if response.status == "ok" else MECResStatus.FAILED
        value = MECJob(response.jid) if status == MECResStatus.OK else response.message

        return (status, value)

    def get_job_info(self, job_id: str) -> tuple[MECResStatus, tuple[str, str]]:
        response: swagger_client.ResponseJobInfo = self._job_api.pleiades_job_info(
            j_id=job_id
        )

        status = MECResStatus.OK if response.status == "ok" else MECResStatus.FAILED
        response = response.to_dict()
        value = (
            (response["job_input_id"], response["lambda_id"])
            if status == MECResStatus.OK
            else (response.message, None)
        )

        return (status, value)
