from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RespDataCreate:
    code: int
    status: str
    message: str
    id: str
    checksum: str


@dataclass(frozen=True, slots=True)
class RespDataMeta:
    code: int
    status: str
    message: str
    id: str
    checksum: str
