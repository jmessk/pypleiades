import logging
import asyncio

from pymec import PleiadesClient


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]:[%(module)s::%(funcName)s()]: %(message)s",
)


async def main():
    # Create a client
    client = PleiadesClient(SERVER_URL)

    worker_task = asyncio.create_task(worker(client))
    requester_task = asyncio.create_task(requester(client))

    await asyncio.gather(worker_task, requester_task)


async def worker(client: PleiadesClient):
    # Create a worker
    worker = client.new_worker().set_runtimes(["pymec+echo"])
    await worker.register_async()

    # Wait for a job
    job = await worker.wait_contract_async()

    # Get the lambda and input data
    input_data = await job.get_input().get_data_async()

    # Process the data
    input_data = input_data.decode("utf-8")
    output_data = f"{input_data}, World!".encode("utf-8")

    # Finish the job and send the output data to the requester
    await job.finish_async(client.new_blob().from_bytes(output_data))


async def requester(client: PleiadesClient):
    # Get the lambda id
    lambda_ = (
        client.new_lambda()
        .set_blob(client.new_blob().from_bytes(b"pymec echo"))
        .set_runtime("pymec+echo")
    )

    input_blob = client.new_blob().from_bytes(b"Hello")

    # Create a job
    job = (
        await client.new_job()
        .set_lambda(lambda_)
        .set_input(input_blob)
        .set_tags(["python3.10"])
        .run_async()
    )

    # Wait until the job is finished
    await job.wait_async("Finished", 5)

    # Get the output data
    output = await job.get_output().get_data_async()
    print(output)


if __name__ == "__main__":
    asyncio.run(main())
