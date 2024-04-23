from dataclasses import dataclass


@dataclass(frozen=True)
class RequestPostJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`
    """

    input_id: str
    functio: str
    extra_tag: list[str]


@dataclass(frozen=True)
class ResponsePostJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`
    """

    code: int
    status: str
    jid: str


@dataclass(frozen=True)
class ResponseGetJobMetadata:
    """Get job metadata
    method: `GET`
    endpoint: `/job/{jid}`
    """

    code: int
    status: str
    job_id: str
    job_status: str
    job_input_id: str
    job_output_id: str


@dataclass(frozen=True)
class RequestPostJobMetadata:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{jid}`
    """
    output: str
    status: str


@dataclass(frozen=True)
class ResponsePostJobMetadata:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{jid}`
    """

    code: int
    status: str
    message: str
