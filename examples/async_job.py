import time
import logging
import asyncio


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]:[%(module)s::%(funcName)s()]: %(message)s",
    )

    worker_task = asyncio.create_task(worker())
    requester_task = asyncio.create_task(requester())

    await asyncio.gather(worker_task, requester_task)


async def worker():
    from pymec.mec_worker import AsyncMECWorker

    server_url = "https://mecrm.dolylab.cc/api/v0.5"

    # Create a worker
    worker = AsyncMECWorker(server_url)

    # Register the worker
    await worker.register(
        [
            "pymec+echo",
        ]
    )
    # print(worker.get_info())

    # Wait for a job
    while (job := await worker.contract()) is None:
        pass

    # print(await job.get_info())

    # Get the lambda and input data
    input_data = await job.get_input_data()
    # lambda_data = job.get_lambda_data()
    # _, input_data = job.get_lambda_and_input_data()

    # Process the data
    input_data = input_data.decode("utf-8")
    output_data = f"{input_data}, World!".encode("utf-8")

    # Finish the job and send the output data to the requester
    await job.finish(output_data)


async def requester():
    from pymec.mec_requester import AsyncMECRequester

    # Wait for the worker to start
    await asyncio.sleep(1)

    server_url = "https://mecrm.dolylab.cc/api/v0.5"

    # Get the lambda id
    lambda_id = await get_lambda_id(server_url, "pymec+echo")

    # Create a requester
    requester = AsyncMECRequester(server_url)

    # Post input data
    input_data_id = await requester.post_data(b"Hello")

    # Create a job
    job = await requester.create_job_by_id(lambda_id, input_data_id)
    # print(await job.get_info())

    # Wait until the job is finished
    while not await job.is_finished():
        time.sleep(0.1)

    # Get the output data
    output = await job.get_output_data()
    print(output)


async def get_lambda_id(server_url: str, runtime: str) -> str:
    from pymec.mec_developer import AsyncMECDeveloper

    # Create a developer
    developer = AsyncMECDeveloper(server_url)

    # Post lambda code and create a lambda
    lambda_data_id = await developer.post_data(b"dummy lambda")
    lambda_id = await developer.create_lambda_by_id(lambda_data_id, runtime)

    return lambda_id


if __name__ == "__main__":
    asyncio.run(main())
