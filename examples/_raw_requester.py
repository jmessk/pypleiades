import asyncio
import logging
import dotenv
from pleiades import Client, api


logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv(override=True)


async def main():
    # client = Client.builder().host("https://mecrm.dolylab.cc/api/v0.5/").build()
    client = Client.default()

    # create lambda
    lambda_ = await client.call_api(
        api.lambda_.Create(data_id="1", runtime="pleiades+example")
    )

    # input
    input = await client.api.data.upload(b"example input")

    # job
    job = await client.api.job.create(lambda_.lambda_id, input.data_id)

    # wait for finish
    job_info = await client.api.job.info(job.job_id, except_="Finished", timeout=10)

    # output
    _ = await client.api.data.download(job_info.output.data_id)

    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
