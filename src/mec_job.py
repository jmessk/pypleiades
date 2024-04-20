import swagger_client
from mec_io import MECIO
from enum import Enum, auto


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

    def get_lambda_and_data(self) -> tuple[str, str]:
        response: swagger_client.ResponseJobInfo = self._job_api.pleiades_job_info(
            j_id=self.job_id
        )

        print(response)

        response = response.to_dict()
        input_lambda = self.get_data(response["lambda_id"])
        input_data = self.get_data(response["job_input_id"])

        return (input_lambda, input_data)

    def finish(self, output_data):
        output_data_id = self.post_data(output_data)

        request = swagger_client.RequestJobUpdate(
            output=output_data_id, status="finished"
        )

        response = self._job_api.pleiades_job_update(self.job_id, body=request)

        print(response)

    def get_status(self) -> tuple[MECJobStatus, str]:
        response: swagger_client.ResponseJobInfo = self._job_api.pleiades_job_info(
            j_id=self.job_id
        ).to_dict()

        print(response.to_dict())

        match response.status:
            case "enqueued":
                return (MECJobStatus.ENQUEUED, response.message)
            case "running":
                return (MECJobStatus.RUNNING, response.message)
            case "error":
                return (MECJobStatus.ERROR, response.message)
            
            case "finished":
                output_data_id = response.to_dict()["job_output_id"]
                output_data = self.get_data(output_data_id)
                
                return (MECJobStatus.FINISHED, output_data)
            
            case _:
                return (MECJobStatus.ERROR, response.message)
    