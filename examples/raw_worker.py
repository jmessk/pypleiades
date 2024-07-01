import asyncio
import httpx

from pymec.api import *


async def main():
    client = httpx.AsyncClient(timeout=20)
    # host = "https://mecrm.dolylab.cc/api/v0.5-snapshot/"
    # host = "http://192.168.168.127:8332/api/v0.5/"
    host = "http://pleiades.local:8332/api/v0.5/"

    worker_register = await WorkerRegisterRequest(
        runtimes=["mecrs+bench"],
    ).send(client, host)

    worker_contract = await WorkerContractRequest(
        worker_id=worker_register.worker_id,
        tags=[],
        timeout=10,
    ).send(client, host)

    if worker_contract.job_id is None:
        print("No job available")
        return

    job_info = await JobInfoRequest(job_id=worker_contract.job_id).send(client, host)

    output_blob = await DataUploadRequest(b"").send(client, host)

    job_update = await JobUpdateRequest(
        job_id=worker_contract.job_id,
        data_id=output_blob.data_id,
        status="finished",
    ).send(client, host)


if __name__ == "__main__":
    asyncio.run(main())
