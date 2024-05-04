from attrs import define, field


@define(slots=True, frozen=True)
class ReqWorkerRegist:
    """Register a worker
    method: `POST`
    endpoint: `/worker`

    type reqMsgWorkerRegist struct {
        Execulator []string `json:"runtime"`
    }
    """

    runtime: list[str]


@define(slots=True, frozen=True)
class RespWorkerRegist:
    """Register a worker
    method: `POST`
    endpoint: `/worker`

    type respWorkerRegist struct {
        Code       int      `json:"code"`
        Status     string   `json:"status"`
        Message    string   `json:"message,omitempty"`
        WorkerId   int64    `json:"id,string,omitempty"`
        Execulator []string `json:"runtime,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    worker_id: str = field(alias="id")
    runtimes: list[str] = field(alias="runtime")


###############################################################


@define(slots=True, frozen=True)
class ReqWorkerContract:
    """Contract a worker
    method: `POST`
    endpoint: `/worker/{worker_id}/contract`

    type reqMsgWorkerContract struct {
        WorkerId int64    `json:"id,string,omitempty"`
        ExtraTag []string `json:"tags,omitempty"`
        MaxTimeo int      `json:"timeout,omitempty"`
    }
    """

    worker_id: str
    tags: list[str]
    timeout: int

    def to_dict(self):
        return {
            "id": self.worker_id,
            "tags": self.tags,
            "timeout": self.timeout,
        }


@define(slots=True, frozen=True)
class RespWorkerContract:
    """Contract a worker
    method: `POST`
    endpoint: `/worker/{worker_id}/contract`

    type respMsgWorkerContract struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`
        JobId   *int64 `json:"job,string,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    job_id: str = field(alias="id")


###############################################################


@define(slots=True, frozen=True)
class RespWorkerInfo:
    """Get worker metadata
    method: `GET`
    endpoint: `/worker/{worker_id}`

    type respMsgWorkerInfo struct {
        Code       int      `json:"code"`
        Status     string   `json:"status"`
        Message    string   `json:"message,omitempty"`
        WorkerId   int64    `json:"id,string,omitempty"`
        Execulator []string `json:"runtime,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    worker_id: str = field(alias="id")
    runtimes: list[str] = field(alias="runtime")
