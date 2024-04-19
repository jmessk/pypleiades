import swagger_client
from enum import Enum, auto
import json


def is_json_value(target_str: str) -> bool:
    try:
        json.loads(target_str)
    except json.JSONDecodeError:
        return False
    return True


class MECResStatus(Enum):
    OK = auto()
    FAILED = auto()


class MECIO(object):
    def __init__(self, client: swagger_client.ApiClient):
        self._client = client
        self._blob_data_api = swagger_client.BlobDataApi(client)

    def get_data(self, data_id: str) -> tuple[MECResStatus, str]:
        response = self._blob_data_api.pleiades_data_download(data_id)

        status = MECResStatus.FAILED if is_json_value(response) else MECResStatus.OK
        value = (
            response if status == MECResStatus.OK else json.loads(response)["message"]
        )

        return (status, value)

    def post_data(self, file: str) -> tuple[MECResStatus, str]:
        response: swagger_client.ResponseDataUpload = (
            self._blob_data_api.pleiades_data_upload(file=file)
        )

        status = MECResStatus.OK if response.status == "ok" else MECResStatus.FAILED
        value = response.id if status == MECResStatus.OK else "Failed to upload data."

        return (status, value)
