import asyncio
import logging
from pymec import Client, api


logging.basicConfig(level=logging.INFO)


async def main():
    client = Client.builder().host("http://pleiades.local/api/v0.5/").build()

    script_data = b"""
        print('Hello, World!')
    """

    # upload user-defined script as blob
    script = await client.call_api(api.data.Upload(data=script_data))

    # create lambda
    lambda_ = await client.call_api(
        api.lambda_.Create(data_id=script.data_id, runtime="pymec+example")
    )

    # input
    input = await client.call_api(api.data.Upload(data=b"example input"))

    # job
    job = await client.call_api(
        api.job.Create(
            lambda_id=lambda_.lambda_id,
            input_id=input.data_id,
            tags=[],
        )
    )

    # wait for finish
    job_info = await client.call_api(
        api.job.Info(
            job_id=job.job_id,
            except_="Finished",
            timeout=10,
        )
    )

    # output
    output = await client.call_api(api.data.Download(data_id=job_info.output.data_id))
    print(output.data)

    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
