import swagger_client
from enum import Enum, auto
import json


def is_json_value(target_str: str) -> bool:
    try:
        json.loads(target_str)
    except json.JSONDecodeError:
        return False
    return True


class MECIOException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECResStatus(Enum):
    OK = auto()
    FAILED = auto()


class MECIO(object):
    def __init__(self, client: swagger_client.ApiClient):
        self._client = client
        self._blob_data_api = swagger_client.BlobDataApi(client)

    def get_data(self, data_id: str) -> str:
        response = self._blob_data_api.pleiades_data_download(data_id)

        if not is_json_value(response):
            return response
        
        raise MECIOException("Failed to get data.")

    def post_data(self, file: str) -> str:
        response: swagger_client.ResponseDataUpload = (
            self._blob_data_api.pleiades_data_upload(file=file)
        )

        if response.status == "ok":
            return response.id
        
        raise MECIOException("Failed to upload data.")
