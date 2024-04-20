import swagger_client
from mec_io import MECIO, MECResStatus
from mec_job import MECJob


class MECRequesterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECRequester(MECIO):
    def __init__(self, client: swagger_client.ApiClient):
        super().__init__(client)

        self._lambda_api = swagger_client.LambdaFunctionsApi(client)
        self._job_api = swagger_client.JobApi(client)

    def create_lambda(self, lambda_id: str, runtime: str) -> str:
        request = swagger_client.RequestFunctionCreate(
            code_id=lambda_id, runtime=runtime
        )

        response: swagger_client.ResponseFunctionCreate = (
            self._lambda_api.pleiades_lambda_create(body=request)
        )

        if response.id is None:
            raise MECRequesterException("Failed to create lambda.")

        return response.id

    def create_job(self, lambda_id: str, input_data_id: str) -> MECJob:
        request = swagger_client.RequestJobCreate(
            input_id=input_data_id, functio=lambda_id
        )

        response: swagger_client.ResponseJobCreate = self._job_api.pleiades_job_create(
            body=request
        )

        print(response)

        return MECJob(self._client, response.jid)
