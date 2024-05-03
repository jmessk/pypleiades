from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`
    """

    codex: str
    runtime: str


@dataclass(frozen=True, slots=True)
class RespLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`
    """

    code: int
    status: str
    id: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespLambdaMeta:
    """Get lambda metadata
    method: `GET`
    endpoint: `/lambda/{lambda_id}`
    """

    code: int
    status: str
    message: str
    id: str
    codex: str
    runtime: str
