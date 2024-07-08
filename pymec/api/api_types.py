from enum import IntEnum

from pydantic import BaseModel
import httpx


class Request(BaseModel):
    def endpoint(self):
        raise NotImplementedError

    async def send(self, client: httpx.AsyncClient, host: str):
        raise NotImplementedError


class Response(BaseModel):
    @staticmethod
    def from_response(response: httpx.Response):
        raise NotImplementedError


class Code(IntEnum):
    OK = 0
    ERROR = 1
    NO_JOB = 1299
