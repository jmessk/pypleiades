from pymec import api, PleiadesClient
import logging
import asyncio

from test_timer import Timer

SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
# SERVER_URL = "http://172.21.39.32:8332/api/v0.5"
# SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"
NUM = 10


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def main():
    data_api = api.data_api.DataAPI(SERVER_URL, logger=logger)
    lambda_api = api.lambda_api.LambdaAPI(SERVER_URL, logger=logger)
    job_api = api.job_api.JobAPI(SERVER_URL, logger=logger)

    # client = PleiadesClient(SERVER_URL, logger=logger)

    queue = asyncio.Queue()

    for _ in range(NUM):
        t = asyncio.create_task(raw(queue, data_api, lambda_api, job_api))
        # t = asyncio.create_task(lib(queue, client))
        await queue.put(t)

        # await asyncio.sleep(1)

    await queue.join()


async def raw(
    queue: asyncio.Queue,
    data_api: api.data_api.DataAPI,
    lambda_api: api.lambda_api.LambdaAPI,
    job_api: api.job_api.JobAPI,
):
    # job_start = Timer("job")

    # lambda
    # start = Timer("\tpost_data_lib")
    labmda_data = await data_api.post_data_async(b"")
    # start.finish()

    lambda_ = await lambda_api.create_async(labmda_data.unwrap().data_id, "bench+pymec")

    # input
    # start = Timer("\tpost_data_lib")
    input_data = await data_api.post_data_async(b"")
    # start.finish()

    # job create
    job = await job_api.create_async(
        lambda_.unwrap().lambda_id,
        input_data.unwrap().data_id,
        [],
    )

    # job wait
    job = await job_api.info_async(job.unwrap().job_id, "Finished", 10)

    # Get the output data
    # get_timer = Timer("\tget_data_lib")
    _ = await data_api.get_data_async(job.unwrap().output.data_id)
    # get_timer.finish()

    # job_start.finish()
    queue.task_done()


# async def lib(queue: asyncio.Queue, client: PleiadesClient):
#     timer = Timer("requester")

#     # Create a lambda
#     lambda_ = await (
#         client.new_lambda()
#         .set_blob(client.new_blob().from_bytes(b""))
#         .set_runtime("bench+pymec")
#         .upload_async()
#     )

#     # Create a input blob
#     input_blob = await client.new_blob().from_bytes(b"").upload_async()

#     # Create a job
#     job = await (
#         client.new_job()
#         .set_lambda(lambda_)
#         .set_input(input_blob)
#         .set_tags(["python3.10"])
#         .run_async()
#     )

#     await job.wait_async("Finished", 5)

#     # Get the output data
#     _ = await job.get_output().get_data_async()

#     timer.finish()
#     queue.task_done()


if __name__ == "__main__":
    asyncio.run(main())
