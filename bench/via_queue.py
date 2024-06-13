from pymec import api
from pymec.mec_job import MECJob
import logging
import threading
import asyncio

from test_timer import Timer


SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
# SERVER_URL = "http://172.21.39.32:8332/api/v0.5"
# SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logging.basicConfig(level=logging.DEBUG)


q_flag = False


def q_thread():
    global q_flag
    while True:
        q = input()
        if q == "q":
            q_flag = True
            print("q_flag is True")
            break


t = threading.Thread(target=q_thread)
t.start()


# APIs
worker_api = api.worker_api.WorkerAPI(SERVER_URL, logger=logger)
job_api = api.job_api.JobAPI(SERVER_URL, logger=logger)
data_api = api.data_api.DataAPI(SERVER_URL, logger=logger)


async def main():
    # Create a job queue
    job_queue = asyncio.Queue()

    # Create a worker
    worker = await worker_api.register_async(["bench+pymec"])

    # Create a worker task
    contractors = []
    for _ in range(16):
        task = asyncio.create_task(contractor(worker.unwrap().worker_id, job_queue))
        contractors.append(task)

    await asyncio.gather(
        asyncio.create_task(worker_spawner(job_queue)),
        *contractors,
    )
    print("Down main")


# contranctor
async def contractor(worker_id: str, job_queue: asyncio.Queue):
    while not q_flag:
        contrancted = await worker_api.contract_async(worker_id, [], 5)
        job_id = contrancted.unwrap().job_id
        if job_id is None:
            continue

        await job_queue.put(job_id)

    print("Down contranctor")


async def worker_spawner(job_queue: asyncio.Queue):
    task_queue = asyncio.Queue()

    while not (q_flag and job_queue.empty()):
        try:
            job_id = job_queue.get_nowait()
        except Exception:
            # await asyncio.sleep(0.05)
            continue
        print(f"Task {job_id} start")
        task = asyncio.create_task(processor(job_id, task_queue))
        await task_queue.put(task)

    print("Joining task queue")
    await task_queue.join()
    print("Down worker_spawner")


# worker task
async def processor(job_id: str, task_queue: asyncio.Queue):
    # Get job info
    job_info = await job_api.info_async(job_id)

    # Get input data
    inpub_id = job_info.unwrap().input.data_id
    _ = await data_api.get_data_async(inpub_id)

    # Post output data
    output_data = await data_api.post_data_async(b"")
    _ = await job_api.update_async(
        job_id,
        output_data.unwrap().data_id,
        "Finished",
    )

    task_queue.task_done()
    print(f"Task {job_id} done")


if __name__ == "__main__":
    asyncio.run(main())
