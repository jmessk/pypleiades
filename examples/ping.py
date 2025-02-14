import asyncio
from pymec import Client


async def main():
    client = Client.builder().host("https://mecrm.dolylab.cc/api/v0.5/").build()

    print(await client.ping())


if __name__ == "__main__":
    asyncio.run(main())
