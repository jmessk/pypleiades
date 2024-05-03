from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`
    """

    data_id: str
    runtime: str


@dataclass(frozen=True, slots=True)
class RespLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`
    """

    code: int
    status: str
    lambda_id: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespLambdaInfo:
    """Get lambda metadata
    method: `GET`
    endpoint: `/lambda/{lambda_id}`
    """

    code: int
    status: str
    message: str
    lambda_id: str
    data_id: str
    runtime: str
