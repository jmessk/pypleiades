from httpx import AsyncClient

from . import data, lambda_, job, worker


class Api:
    __slots__ = ["__client", "_data", "_lambda", "_job", "_worker"]

    def __init__(self, client: AsyncClient):
        self.__client = client

        self._data = data.Data(self.__client)
        self._lambda = lambda_.Lambda(self.__client)
        self._job = job.Job(self.__client)
        self._worker = worker.Worker(self.__client)

    @property
    def data(self) -> data.Data:
        return self._data

    @property
    def lambda_(self) -> lambda_.Lambda:
        return self._lambda

    @property
    def job(self) -> job.Job:
        return self._job

    @property
    def worker(self) -> worker.Worker:
        return self._worker
