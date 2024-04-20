import swagger_client
from mec_io import MECIO
from enum import Enum, auto

import http.client
import json


class MECJobException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECJobStatus(Enum):
    ENQUEUED = auto()
    RUNNING = auto()
    FINISHED = auto()
    ERROR = auto()


class MECJob(MECIO):
    def __init__(
        self,
        client: swagger_client.ApiClient,
        job_id: str | None = None,
    ):
        super().__init__(client)
        self._job_api = swagger_client.JobApi(client)
        self.job_id = job_id

        # Temporary client until API is updated
        self._connection = http.client.HTTPSConnection("mecrm.dolylab.cc")

    def get_info(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
        }

        self._connection.request("GET", f"/api/v0.5/job/{self.job_id}", headers=headers)
        response = self._connection.getresponse()

        data = response.read().decode("utf-8")

        return json.loads(data)

    def get_lambda_and_data(self) -> tuple[str, str]:
        response = self.get_info()

        input_lambda = self.get_data(response["lambda_id"])
        input_data = self.get_data(response["job_input_id"])

        return (input_lambda, input_data)

    def finish(self, output_data):
        # output_data_id = self.post_data(output_data)
        output_data_id = self.post_data("./sample.txt")

        request = swagger_client.RequestJobUpdate(
            output=output_data_id, status="finished"
        )

        response = self._job_api.pleiades_job_update(self.job_id, body=request)

        print(response)

    def is_finished(self) -> bool:
        response = self.get_info()

        return response["job_status"] == "Finished"
