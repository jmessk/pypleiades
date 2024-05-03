from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RespDataCreate:
    """Create a BLOB
    method: `POST`
    endpoint: `/data`
    """

    code: int
    status: str
    message: str
    id: str
    checksum: str


###############################################################


@dataclass(frozen=True, slots=True)
class RespDataMeta:
    """Get BLOB metadata
    method: `GET`
    endpoint: `/data/{data_id}`
    """

    code: int
    status: str
    message: str
    id: str
    checksum: str
