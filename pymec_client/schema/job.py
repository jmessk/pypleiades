from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`
    """

    input: str
    lambda: str
    tags: list[str]


@dataclass(frozen=True, slots=True)
class ResJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`
    """

    code: int
    status: str
    message: str
    id: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespJobMeta:
    """Get job metadata
    method: `GET`
    endpoint: `/job/{job_id}`
    """

    code: int
    status: str
    message: str
    id: str
    job_status: str
    job_input_id: str
    job_output_id: str
    functio: str
    runtime: str
    # new
    tags: list[str]
    lambda: str
    input: str
    output: str
    state: str


###############################################################


@dataclass(frozen=True, slots=True)
class ReqJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`
    """

    output: str
    status: str
    state: str


@dataclass(frozen=True, slots=True)
class RespJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`
    """

    code: int
    status: str
    message: str
