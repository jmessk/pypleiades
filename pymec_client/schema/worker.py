from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqWorkerRegist:
    """Register a worker
    method: `POST`
    endpoint: `/worker`
    """

    runtime: list[str]


@dataclass(frozen=True, slots=True)
class RespWorkerRegist:
    """Register a worker
    method: `POST`
    endpoint: `/worker`
    """

    code: int
    status: str
    message: str
    worker_id: str
    runtimes: list[str]


###############################################################


@dataclass(frozen=True, slots=True)
class ReqWorkerContract:
    """Contract a worker
    method: `POST`
    endpoint: `/worker/{worker_id}/contract`
    """

    worker_id: str
    tags: list[str]
    timeout: int


@dataclass(frozen=True, slots=True)
class RespWorkerContract:
    """Contract a worker
    method: `POST`
    endpoint: `/worker/{worker_id}/contract`
    """

    code: int
    status: str
    message: str
    job_id: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespWorkerInfo:
    """Get worker metadata
    method: `GET`
    endpoint: `/worker/{worker_id}`
    """

    code: int
    status: str
    message: str
    worker_id: str
    runtimes: list[str]
