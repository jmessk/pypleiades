from attrs import define, field

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
@define(slots=True, frozen=True)
class Job:
    jid: str = field(alias="job_id")


job = Job("1234")
print(job)


# test 3
@define(slots=True, frozen=True)
class Data:
    data_id: str

    def to_dict(self):
        return {"id": self.data_id}

data = Data("1234")
print(data.to_dict())
