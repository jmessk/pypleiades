import httpx
import logging
from pydantic import Field

from .. import type


class Response(type.Response):
    code: int
    status: str
    job_id: str = Field(alias="id")

    def from_response(response: httpx.Response) -> "Response":
        return Response(**response.json())


class Request(type.Request[Response]):
    lambda_id: str = Field(serialization_alias="lambda")
    data_id: str = Field(serialization_alias="input")
    tags: list[str]

    def endpoint(self):
        return "job"

    async def send(self, client: httpx.AsyncClient) -> Response:
        logging.debug(f"Creating job: {self}")

        response = await client.post(
            self.endpoint(),
            json=self.model_dump(by_alias=True),
        )
        deserialized = Response.from_response(response)

        logging.debug(f"Created job: {deserialized}")
        return deserialized
