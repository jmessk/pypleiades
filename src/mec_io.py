# import swagger_client
from enum import Enum, auto
import requests


# def is_json_value(target_str: str) -> bool:
#     try:
#         json.loads(target_str)
#     except json.JSONDecodeError:
#         return False
#     return True


class MECIOException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MECResStatus(Enum):
    OK = auto()
    FAILED = auto()


class MECIO(object):
    def __init__(self, server_url: str):
        self._server_url = server_url

    def get_data(self, data_id: str) -> str:

        endpoint = f"{self._server_url}/data/{data_id}/blob"
        headers = {"Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
        )

        # blob が json の場合は成功したのか判定できない
        return response.text
    
    def post_data(self, data: str, filename: str ="input.txt") -> str:
        endpoint = f"{self._server_url}/data"
        headers = {"Accept": "application/json"}

        file = { "file": (filename, data) }

        response = requests.post(
            endpoint,
            headers=headers,
            files=file,
        )

        response_json: dict[str, str] = response.json()

        if response_json.get("status") != "ok":
            print(response_json)
            raise MECIOException("Failed to upload data.")
        
        return response_json["id"]

    # def post_local_file(self, path: str) -> str:
        # headers = {"Accept": "application/json"}

        # self._connection.request(
        #     "POST",
        #     "/api/v0.5/data",
        #     headers=headers,
        #     body=open(path, "rb").read(),
        # )

        # response = self._connection.getresponse()
        # data = response.read().decode("utf-8")

        # response_json: dict[str, str] = json.loads(data)

        # if response_json.get("id") is not None:
        #     return response_json["id"]

        # raise MECIOException("Failed to upload data.")

        # response: swagger_client.ResponseDataUpload = (
        #     self._blob_data_api.pleiades_data_upload(file=path)
        # )

        # if response.status == "ok":
        #     return response.id

        # raise MECIOException("Failed to upload data.")
