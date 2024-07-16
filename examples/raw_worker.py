import asyncio
import httpx

import pymec
from pymec import api


async def main():
    client = (
        pymec.Client()
        .client(httpx.AsyncClient(timeout=20))
        # .host("https://mecrm.dolylab.cc/api/v0.5-snapshot/")
        .host("http://192.168.168.127:8332/api/v0.5/")
        # .host("http://pleiades.local:8332/api/v0.5/")
        # .host("http://192.168.1.22/api/v0.5/")
    )

    # register worker
    register = await client.request(api.WorkerRegisterRequest(runtimes=["test+pymec"]))

    print(register)

    # contract job
    contract = await client.request(
        api.WorkerContractRequest(
            worker_id=register.worker_id,
            tags=[],
            timeout=10,
        )
    )

    print(contract)

    if contract.job_id is None:
        print("No job available")
        return

    # job info
    job_info = await client.request(api.JobInfoRequest(job_id=contract.job_id))

    print(job_info)

    # input
    _ = await client.request(api.DataDownloadRequest(data_id=job_info.input.data_id))

    # output
    output = await client.request(api.DataUploadRequest(data=b""))

    # job update
    _ = await client.request(
        api.JobUpdateRequest(
            job_id=contract.job_id,
            data_id=output.data_id,
            status="finished",
        )
    )

    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
