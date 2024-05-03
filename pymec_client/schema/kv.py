from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReqKVNamespaceCreate:
    pass


@dataclass(frozen=True, slots=True)
class ReqKVNamespaceCreate:
    code: int
    status: str
    namespace: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespKVNamespaceInfo:
    code: int
    status: str
    kv_id: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespKVGet:
    code: int
    status: str
    value: str


###############################################################


@dataclass(frozen=True, slots=True)
class ReqKVSet:
    value: str


@dataclass(frozen=True, slots=True)
class RespKVSet:
    code: int
    status: str
    value: str
