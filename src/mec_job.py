# import swagger_client
from mec_io import MECIO
from enum import Enum, auto

import requests


class MECJobException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECJobStatus(Enum):
    ENQUEUED = auto()
    RUNNING = auto()
    FINISHED = auto()
    ERROR = auto()


class MECJob(MECIO):
    # def __init__(
    #     self,
    #     client: swagger_client.ApiClient,
    #     job_id: str | None = None,
    # ):
    #     super().__init__(client)
    #     self._job_api = swagger_client.JobApi(client)
    #     self.job_id = job_id

    #     # Temporary client until API is updated
    #     self._connection = http.client.HTTPSConnection("mecrm.dolylab.cc")

    # def __init__(
    #     self,
    #     connection: http.client.HTTPSConnection,
    #     job_id: str,
    # ):
    #     self._connection = connection
    #     self._job_id = job_id

    #     self._job_api = swagger_client.JobApi()
    #     self._blob_data_api = swagger_client.BlobDataApi()

    def __init__(self, server_url: str, job_id: str):
        super().__init__(server_url)
        self._job_id = job_id

    def get_info(self) -> dict[str, str]:
        # headers = {"Accept": "application/json"}

        # self._connection.request(
        #     "GET",
        #     f"/api/v0.5/job/{self._job_id}",
        #     headers=headers,
        # )
        # response = self._connection.getresponse()

        # data = response.read().decode("utf-8")

        # return json.loads(data)

        endpoint = f"{self._server_url}/job/{self._job_id}"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        return response.json()

    def get_lambda_and_input_data(self) -> tuple[str, str]:
        response = self.get_info()

        input_lambda = self.get_data(response["lambda_id"])
        input_data = self.get_data(response["job_input_id"])

        return (input_lambda, input_data)

    def finish(self, data: str):
        # output_data_id = self.post_data(output_data)
        # output_data_id = self.post_local_file(path)

        # request = swagger_client.RequestJobUpdate(
        #     output=output_data_id, status="finished"
        # )

        # self._job_api.pleiades_job_update(self._job_id, body=request)

        output_data_id = self.post_data(data, "output.txt")

        endpoint = f"{self._server_url}/job/{self._job_id}"
        headers = {"Accept": "application/json"}

        body_json = {
            "output": output_data_id,
            "status": "finished",
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            print(response_json)
            raise MECJobException("Failed to finish job.")

    def is_finished(self) -> bool:
        response = self.get_info()

        return response["job_status"] == "Finished"
        
    def get_output_data(self) -> str:
        response = self.get_info()
        output_data = self.get_data(response["job_output_id"])

        return output_data
