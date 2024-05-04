from attrs import define, field


@define(slots=True, frozen=True)
class ReqLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`

    type reqMsgFunctioCreate struct {
        CodeId int64  `json:"codex,string"`
        Runt   string `json:"runtime,omitempty"`
    }
    """

    data_id: str
    runtime: str

    def to_dict(self):
        return {
            "codex": self.data_id,
            "runtime": self.runtime,
        }


@define(slots=True, frozen=True)
class RespLambdaCreate:
    """Create a lambda
    method: `POST`
    endpoint: `/lambda`

    type respMsgFunctioCreate struct {
        Code   int    `json:"code"`
        Status string `json:"status"`
        Id     int64  `json:"id,string"`
    }
    """

    code: int
    status: str
    lambda_id: str = field(alias="id")


###############################################################


@define(slots=True, frozen=True)
class RespLambdaInfo:
    """Get lambda metadata
    method: `GET`
    endpoint: `/lambda/{lambda_id}`

    type respMsgFunctioRead struct {
        Code      int    `json:"code"`
        Status    string `json:"status"`
        Message   string `json:"message,omitempty"`
        FunctioId int64  `json:"id,string,omitempty"`
        CodeId    int64  `json:"codex,string,omitempty"`
        Runt      string `json:"runtime,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    lambda_id: str = field(alias="id")
    data_id: str = field(alias="codex")
    runtime: str
