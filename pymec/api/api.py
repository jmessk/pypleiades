from enum import IntEnum
from typing import TypeVar, Generic
from pydantic import BaseModel
import httpx

from . import data, lambda_, job, worker

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


class Api:
    __slots__ = ["__client, __data, __lambda, __job, __worker"]

    def __init__(self):
        self.__client = httpx.AsyncClient()

        self.__data = data.Data(self.__client)
        self.__lambda = lambda_.Lambda(self.__client)
        self.__job = job.Job(self.__client)
        self.__worker = worker.Worker(self.__client)

    @property
    def data(self) -> data.Data:
        return self.__data

    @property
    def lambda_(self) -> lambda_.Lambda:
        return self.__lambda

    @property
    def job(self) -> job.Job:
        return self.__job

    @property
    def worker(self) -> worker.Worker:
        return self.__worker
