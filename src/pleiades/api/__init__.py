from httpx import AsyncClient

from . import data, lambda_, job, worker


class Api:
    __slots__ = ["__client", "__data", "__lambda", "__job", "__worker"]

    def __init__(self, client: AsyncClient):
        self.__client = client

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
