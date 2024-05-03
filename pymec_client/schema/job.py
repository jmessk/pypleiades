from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`
    """

    input: str
    lambda_id: str
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
    job_id: str


###############################################################


@dataclass(frozen=True, slots=True)
class Lambda:
    lambda_id: str
    runtime: str
    data_id: str


@dataclass(frozen=True, slots=True)
class RespJobInfo:
    """Get job metadata
    method: `GET`
    endpoint: `/job/{job_id}`
    """

    code: int
    status: str
    message: str
    id: str
    job_status: str
    input_data_id: str
    output_data_id: str
    lambda_id: str
    runtime: str
    # new
    tags: list[str]
    lambda_: Lambda
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

    output_data_id: str
    status: str
    job_status: str


@dataclass(frozen=True, slots=True)
class RespJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`
    """

    code: int
    status: str
    message: str
