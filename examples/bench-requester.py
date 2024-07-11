import asyncio
import httpx
import time

import pymec
from pymec import api


async def main():
    client = (
        pymec.Client()
        .client(httpx.AsyncClient(timeout=20))
        # .host("https://mecrm.dolylab.cc/api/v0.5-snapshot/")
        # .host("http://192.168.168.127:8332/api/v0.5/")
        # .host("http://pleiades.local:8332/api/v0.5/")
        .host("http://192.168.1.22/api/v0.5/")
    )

    # create lambda
    lambda_: api.LambdaCreateResponse = await client.request(
        api.LambdaCreateRequest(
            data_id="1",
            runtime="mecrs+bench",
        )
    )

    lambda_id = lambda_.lambda_id


    INTERVAL_MS = 20
    NUM = 100

    interval = INTERVAL_MS / 1000
    for _ in range(NUM):
        asyncio.create_task(requester(client, lambda_id))
        await asyncio.sleep(interval)


async def requester(client: pymec.Client, lambda_id: str):
    start = time.time()

    # input
    input: api.DataUploadResponse = await client.request(
        api.DataUploadRequest(data=b"")
    )

    # job
    job: api.JobCreateResponse = await client.request(
        api.JobCreateRequest(
            lambda_id=lambda_id,
            data_id=input.data_id,
            tags=[],
        )
    )

    # wait for finish
    job_info: api.JobInfoResponse = await client.request(
        api.JobInfoRequest(
            job_id=job.job_id,
            except_="Finished",
            timeout=10,
        )
    )

    # output
    _: api.DataDownloadResponse = await client.request(
        api.DataDownloadRequest(data_id=job_info.output.data_id)
    )

    print(f"elapsed: {time.time() - start:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
