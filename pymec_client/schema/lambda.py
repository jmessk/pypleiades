from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqLambdaCreate:
    codex: str
    runtime: str


@dataclass(frozen=True, slots=True)
class RespLambdaCreate:
    code: int
    status: str
    id: str


@dataclass(frozen=True, slots=True)
class RespLambdaMeta:
    code: int
    status: str
    id: str
    checksum: str
