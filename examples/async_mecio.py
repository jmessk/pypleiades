import asyncio
import time
from pymec_client.mec_io import MECIO, AsyncMECIO


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5"
TEST_NUM = 5


def main():
    io = MECIO(SERVER_URL)
    ids = []

    start = time.perf_counter()

    for i in range(TEST_NUM):
        data_id = io.post_data(b"Hello")
        print(f"Sync post: {i}")
        ids.append(data_id)

    for data_id in ids:
        io.get_data(data_id)
        print(f"Sync get: {data_id}")

    end = time.perf_counter()
    print(f"Sync: {end - start}")


async def async_main():
    io = AsyncMECIO(SERVER_URL)
    tasks = []
    ids = []

    start = time.perf_counter()

    for i in range(TEST_NUM):
        task = asyncio.create_task(io.post_data(b"Hello"))
        print(f"Async post: {i}")
        tasks.append(task)

    for task in tasks:
        ids.append(await task)

    for data_id in ids:
        await io.get_data(data_id)
        print(f"Async get: {data_id}")

    end = time.perf_counter()
    print(f"Async: {end - start}")


if __name__ == "__main__":
    main()
    print()
    asyncio.run(async_main())
