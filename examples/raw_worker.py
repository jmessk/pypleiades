import asyncio
import logging
from pymec import Client, api


logging.basicConfig(level=logging.INFO)


async def main():
    client = Client.builder().host("http://pleiades.local/api/v0.5/").build()

    # register worker
    register = await client.call_api(api.worker.Register(runtimes=["pymec+example"]))

    # contract job
    contract = await client.call_api(
        api.worker.Contract(
            worker_id=register.worker_id,
            timeout=10,
        )
    )

    if contract.job_id is None:
        print("No job available")
        return

    # job info
    job_info = await client.call_api(api.job.Info(job_id=contract.job_id))

    # user-defined script
    script = await client.call_api(api.data.Download(data_id=job_info.lambda_.data_id))
    print(script.data)

    # input
    input = await client.call_api(api.data.Download(data_id=job_info.input.data_id))
    print(input.data)

    # output
    output = await client.call_api(api.data.Upload(data=b"example output"))

    # job update
    _ = await client.call_api(
        api.job.Update(
            job_id=contract.job_id,
            data_id=output.data_id,
            status="finished",
        )
    )
    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
