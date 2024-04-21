# import swagger_client
from mec_io import MECIO, MECResStatus
from mec_job import MECJob

import requests


class MECRequesterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECRequester(MECIO):
    def __init__(self, server_url: str):
        super().__init__(server_url)

        # self._lambda_api = swagger_client.LambdaFunctionsApi()
        # self._job_api = swagger_client.JobApi()

    def create_lambda(self, lambda_id: str, runtime: str) -> str:
        # request = swagger_client.RequestFunctionCreate(
        #     code_id=lambda_id, runtime=runtime
        # )

        # response: swagger_client.ResponseFunctionCreate = (
        #     self._lambda_api.pleiades_lambda_create(body=request)
        # )

        # if response.id is None:
        #     raise MECRequesterException("Failed to create lambda.")

        # return response.id

        endpoint = f"{self._server_url}/lambda"
        headers = {"Accept": "application/json"}

        body_json = {
            "code_id": lambda_id,
            "runtime": runtime,
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            print(response_json)
            raise MECRequesterException("Failed to create lambda.")
        
        return response_json["id"]

    def create_job(self, lambda_id: str, input_data_id: str) -> MECJob:
        # request = swagger_client.RequestJobCreate(
        #     input_id=input_data_id, functio=lambda_id
        # )

        # response: swagger_client.ResponseJobCreate = self._job_api.pleiades_job_create(
        #     body=request
        # )

        # return MECJob(self._connection, response.jid)

        endpoint = f"{self._server_url}/job"
        headers = {"Accept": "application/json"}

        body_json = {
            "input_id": input_data_id,
            "functio": lambda_id,
            "extra_tag": [],
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=body_json,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            print(response_json)
            raise MECRequesterException("Failed to create job.")
        
        return MECJob(self._server_url, response_json["jid"])
