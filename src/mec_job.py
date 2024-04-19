import swagger_client
from mec_io import MECIO, MECResStatus
from enum import Enum, auto


class MECJobStatus(Enum):
    ENQUEUED = auto()
    RUNNING = auto()
    FINISHED = auto()
    ERROR = auto()


class MECJob(MECIO):
    def __init__(
        self,
        job_id: str | None = None,
        input_data_id: str | None = None,
        lambda_id: str | None = None,
    ):
        super().__init__(swagger_client.ApiClient())
        self._job_api = swagger_client.JobApi(self._client)
        self.job_id = job_id
        self.input_data_id = input_data_id
        self.lambda_id = lambda_id

    def is_finished(self) -> tuple[MECJobStatus, str]:
        response: swagger_client.ResponseJobInfo = self._job_api.pleiades_job_info(
            self.job_id
        )

        match response.status:
            case "enqueued":
                return (MECJobStatus.ENQUEUED, response.message)
            case "running":
                return (MECJobStatus.RUNNING, response.message)
            case "finished": 
                response = response.to_dict()
                status, value = self.get_data(response["job_output_id"])

                if status == MECResStatus.FAILED:
                    return (MECJobStatus.ERROR, "Failed to get job output data.")

                return (MECJobStatus.FINISHED, value)
            
            case "error":
                return (MECJobStatus.ERROR, response.message)
            case _:
                return (MECJobStatus.ERROR, response.message)
