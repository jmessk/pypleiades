import asyncio
import dotenv
from pleiades import Client


dotenv.load_dotenv(override=True)


async def main():
    client = Client.default()
    print(await client.ping())


if __name__ == "__main__":
    asyncio.run(main())
