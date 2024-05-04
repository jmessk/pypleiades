from attrs import define, field


@define(slots=True, frozen=True)
class RespDataCreate:
    """Create a BLOB
    method: `POST`
    endpoint: `/data`

    type respMessageDataCreate struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`

        DataID   int64  `json:"id,string"`
        DataHash string `json:"checksum"`
    }
    """

    code: int
    status: str
    message: str
    data_id: str = field(alias="id")
    checksum: str


###############################################################


@define(slots=True, frozen=True)
class RespDataInfo:
    """Get BLOB metadata
    method: `GET`
    endpoint: `/data/{data_id}`

    type respMsgDataRead struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`

        DataID   int64  `json:"id,string,omitempty"`
        DataHash string `json:"checksum,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    data_id: str = field(alias="id")
    checksum: str
