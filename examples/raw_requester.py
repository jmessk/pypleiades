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

    # create lambda
    lambda_ = await client.api.lambda_.create("0", "pymec+example")

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
