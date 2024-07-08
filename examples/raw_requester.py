import asyncio
import httpx

import pymec
from pymec import api


async def main():
    client = (
        pymec.Client()
        .client(httpx.AsyncClient(timeout=10))
        # .host("https://mecrm.dolylab.cc/api/v0.5-snapshot/")
        .host("http://192.168.168.127:8332/api/v0.5/")
        # .host("http://pleiades.local:8332/api/v0.5/")
    )

    # create lambda
    lambda_: api.LambdaCreateResponse = await client.request(
        api.LambdaCreateRequest(
            data_id="1",
            runtime="test+pymec",
        )
    )

    print(lambda_)

    # input
    input: api.DataUploadResponse = await client.request(
        api.DataUploadRequest(data=b"")
    )

    print(input)

    # job
    job: api.JobCreateResponse = await client.request(
        api.JobCreateRequest(
            lambda_id=lambda_.lambda_id,
            data_id=input.data_id,
            tags=[],
        )
    )

    print(job)

    # wait for finish
    job_info: api.JobInfoResponse = await client.request(
        api.JobInfoRequest(
            job_id=job.job_id,
            except_="Finished",
            timeout=10,
        )
    )

    print(job_info)

    # output
    _: api.DataDownloadResponse = await client.request(
        api.DataDownloadRequest(data_id=job_info.output.data_id)
    )

    print("job finished")


if __name__ == "__main__":
    asyncio.run(main())
