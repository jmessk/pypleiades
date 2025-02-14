import asyncio
import logging
import dotenv
from pleiades import Client


logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv(override=True)


async def main():
    # client = Client.builder().host("https://mecrm.dolylab.cc/api/v0.5/").build()
    client = Client.default()

    # register worker
    register = await client.api.worker.register(runtimes=["pleiades+example"])

    # contract job
    contract = await client.api.worker.contract(register.worker_id, timeout=10)

    if contract.job_id is None:
        print("No job available")
        return

    # job info
    job_info = await client.api.job.info(contract.job_id)

    # user-defined script
    _script = await client.api.data.download(job_info.lambda_.data_id)

    # input
    input = await client.api.data.download(job_info.input.data_id)
    print(input.data)

    # output
    output = await client.api.data.upload(b"example output")

    _ = await client.api.job.update(
        contract.job_id,
        output.data_id,
        "finished",
    )
    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
