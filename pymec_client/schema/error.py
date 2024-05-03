from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RespError:
    """Response error"""

    code: int
    status: str
    message: str
