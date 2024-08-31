import asyncio
import pymec


async def main():
    client = (
        pymec.Client()
        .builder()
        # .host("https://mecrm.dolylab.cc/api/v0.5-snapshot/")
        .host("http://192.168.168.127:8332/api/v0.5/")
        # .host("http://pleiades.local:8332/api/v0.5/")
        # .host("http://192.168.1.22/api/v0.5/")
        .build()
    )

    # register worker
    register = await client.api.worker.register(["pymec+example"])

    # contract job
    contract = await client.api.worker.contract(register.worker_id, 10)

    if contract.job_id is None:
        print("No job available")
        return

    # job info
    job_info = await client.api.job.info(contract.job_id)

    # input
    input = await client.api.data.download(job_info)
    print(input.data)

    # output
    output = await client.api.data.upload(b"example output")

    # job update
    _ = await client.api.job.update(contract.job_id, output.data_id, "Finished")
    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
