import swagger_client
import json


class RegisterException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class DataNotFoundException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class PoseWorker(object):
    def __init__(
        self,
        client: swagger_client.ApiClient,
        server_url="https://mecrm.dolylab.cc/api/v0.5/",
    ):
        self._worker_api = swagger_client.WorkerApi(client)
        self._job_api = swagger_client.JobApi(client)
        self._blob_api = swagger_client.BlobDataApi(client)

    def register(self) -> str:
        request_body = swagger_client.RequestWorkerRegist(["python+openpose+gpu"])

        response_body: str = self._worker_api.pleiades_worker_regist(body=request_body)
        print
        
        response_json: dict[str, str] = json.loads((response_body))

        if response_json["status"] == "ok":
            return response_json["wid"]

        raise RegisterException(response_json["message"])

    def contract(self, worker_id: str) -> str | None:
        request_body = swagger_client.RequestWorkerContract(
            worker_id=worker_id, timeout=20
        )

        response_body: dict[str, str] = self._worker_api.pleiades_worker_contract(
            request_body
        )
        response_json: dict[str, str] = json.loads(response_body)

        return response_json["jid"]

    def get_input_data_id(self, job_id: str) -> str:
        response_body: dict[str, str] = self._job_api.pleiades_job_info(job_id)
        response_json: dict[str, str] = json.loads(response_body)

        return response_json["job_input_id"]

    def get_data(self, data_id: str) -> str | None:
        response_body = self._blob_api.pleiades_data_download(data_id)
        return response_body
