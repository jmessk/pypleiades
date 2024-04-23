from dataclasses import dataclass


@dataclass(frozen=True)
class ResponsePostData:
    """Response
    method: `POST`
    endpoint: `/data`
    """

    code: int
    status: str
    id: str
