from attrs import define, field, converters


# test 1
@define(slots=True, frozen=True)
class Worker:
    worker_id: str = field(alias="wid")
    status: str


response = {
    "wid": "1234",
    "status": "ok",
}

worker = Worker(**response)
print(worker)


# test 2
@define(slots=True, frozen=True, auto_attribs=True)
class Job:
    jid: str = field(alias="job_id")


response = {
    "job_id": "1234",
}

job = Job("1234")
print(job)


# test 3
@define(slots=True, frozen=True, auto_attribs=True)
class Data:
    data_id: str

    def to_dict(self):
        return {"id": self.data_id}


data = Data("1234")
print(data.to_dict())


# # test 4
# @define(slots=True, frozen=True, auto_attribs=True)
# class JobInfo:
#     job: Job = field(factory=Job)
#     id: str

#     # @classmethod
#     # def from_dict(cls, data):
#     #     job = Job(**data["job"])
#     #     print(job)

#     #     return cls(
#     #         job=job,
#     #         **data,
#     #     )


# response = {
#     "job": {"job_id": "1234"},
#     "id": "1234",
# }

# # job_info = JobInfo.from_dict(response)
# job_info = JobInfo(**response)
# print(job_info)


# test 5
from typing import Optional

@define(auto_attribs=True)
class Info:
    data: str
    msg: Optional[str] = None


response = {
    "data": "1234",
}

info = Info(**response)
print(info)
