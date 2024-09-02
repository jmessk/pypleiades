import httpx
import logging
from pydantic import Field

from .. import type


class Response(type.Response):
    code: int
    status: str
    message: str

    def from_response(response: httpx.Response) -> "Response":
        return Response(**response.json())


class Request(type.Request[Response]):
    job_id: str = Field(exclude=True)
    data_id: str = Field(serialization_alias="output")
    status: str = Field(serialization_alias="status")

    def endpoint(self):
        return f"job/{self.job_id}"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Updating job: {self}")

        response = await client.post(
            self.endpoint(),
            json=self.model_dump(by_alias=True),
        )
        deserialized = Response.from_response(response)

        logging.debug(f"Updated job: {deserialized}")
        return deserialized
