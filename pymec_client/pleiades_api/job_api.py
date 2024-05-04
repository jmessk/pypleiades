from attrs import define, field


@define(slots=True, frozen=True)
class ReqJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`

    type reqMsgJobCreate struct {
        InputDataId int64    `json:"input,string"`
        FunctionId  int64    `json:"lambda,string"`
        ExtraTag    []string `json:"tags"`
    }
    """

    data_id: str
    lambda_id: str
    tags: list[str]

    def to_dict(self):
        return {
            "input": self.data_id,
            "lambda": self.lambda_id,
            "tags": self.tags,
        }


@define(slots=True, frozen=True)
class ResJobCreate:
    """Create a job
    method: `POST`
    endpoint: `/job`

    type respMsgJobCreate struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`
        JobId   int64  `json:"id,string,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    job_id: str = field(alias="id")


###############################################################


@define(slots=True, frozen=True)
class Lambda:
    """
    type respJobLambda struct {
        Id      int64  `json:"id,string"`
        Runtime string `json:"runtime"`
        Code    int    `json:"codex"`
    }
    """

    lambda_id: str = field(alias="id")
    runtime: str
    data_id: str = field(alias="codex")


@define(slots=True, frozen=True)
class RespJobInfo:
    """Get job metadata
    method: `GET`
    endpoint: `/job/{job_id}`

    type respMsgJobInfo struct {
        Code              int    `json:"code"`
        Status            string `json:"status"`
        Message           string `json:"message,omitempty"`
        JobId             int64  `json:"id,string,omitempty"`
        JobStatus         string `json:"job_status,omitempty"`
        JobInputData      *int64 `json:"job_input_id,string"`
        JobOutputData     *int64 `json:"job_output_id,string"`
        JobFunctio        int64  `json:"functio,string,omitempty"`
        JobFunctioRuntime string `json:"runtime,omitempty"`
        // New Format
        Tags   []string      `json:"tags,omitempty"`
        Lambda respJobLambda `json:"lambda"`
        Input  *respJobData  `json:"input,omitempty"`
        Output *respJobData  `json:"output,omitempty"`
        State  string        `json:"state,omitempty"`
    }
    """

    code: int
    status: str
    message: str
    job_id: str = field(alias="id")
    job_status: str
    input_data_id: str = field(alias="job_input_id")
    output_data_id: str = field(alias="job_output_id")
    lambda_id: str = field(alias="functio")
    runtime: str
    # new
    tags: list[str]
    lambda_: Lambda
    input: str
    output: str
    state: str


###############################################################


@define(slots=True, frozen=True)
class ReqJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`

    type reqMsgJobUpdate struct {
        id     int64
        Output *int64  `json:"output,string,omitempty"`
        Status *string `json:"status,omitempty"`
        State  *string `json:"state,omitempty"`
    }
    """

    output_data_id: str
    status: str
    job_status: str

    def to_dict(self):
        return {
            "output": self.output_data_id,
            "status": self.status,
            "state": self.job_status,
        }


@define(slots=True, frozen=True)
class RespJobUpdate:
    """Update job metadata
    method: `POST`
    endpoint: `/job/{job_id}`

    type respMsgJobUpdate struct {
        Code    int    `json:"code"`
        Status  string `json:"status"`
        Message string `json:"message,omitempty"`
    }
    """

    code: int
    status: str
    message: str
