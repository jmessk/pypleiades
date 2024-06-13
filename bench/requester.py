from pymec import api
import logging
import threading
import asyncio

from test_timer import Timer

SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
# SERVER_URL = "http://172.21.39.32:8332/api/v0.5"
# SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


q_flag = False


def q_thread():
    global q_flag
    while True:
        q = input()
        if q == "q":
            q_flag = True
            break


t = threading.Thread(target=q_thread)
t.start()


async def main():

    data_api = api.data_api.DataAPI(SERVER_URL, logger=logger)
    lambda_api = api.lambda_api.LambdaAPI(SERVER_URL, logger=logger)
    job_api = api.job_api.JobAPI(SERVER_URL, logger=logger)


async def task(
    queue: asyncio.Queue,
    data_api: api.data_api.DataAPI,
    lambda_api: api.lambda_api.LambdaAPI,
    job_api: api.job_api.JobAPI,
):
    # lambda
    labmda_data = await data_api.post_data_async(b"")
    lambda_ = await lambda_api.create_async(labmda_data.unwrap().data_id, "bench+pymec")

    # input
    input_data = await data_api.post_data_async(b"")

    # job create
    job = await job_api.create_async(
        lambda_.unwrap().lambda_id,
        input_data.unwrap().data_id,
        [],
    )

    # job wait
    _ = await job_api.info_async(job.unwrap().job_id, "Finished", 10)



if __name__ == "__main__":
    asyncio.run(main())
