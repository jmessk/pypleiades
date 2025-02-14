from enum import IntEnum
from typing import TypeVar, Generic
from pydantic import BaseModel
import httpx


R = TypeVar("R", bound="Response")


class Request(BaseModel, Generic[R]):
    def endpoint(self) -> str:
        raise NotImplementedError

    async def send(self, client: httpx.AsyncClient) -> R:
        raise NotImplementedError


class Response(BaseModel):
    @staticmethod
    def from_response(response: httpx.Response) -> R:
        raise NotImplementedError


class Code(IntEnum):
    OK = 0
    ERROR = 1
    NO_JOB = 1299
