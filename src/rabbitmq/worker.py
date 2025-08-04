import asyncio
from .consumer import ParcelConsumer


async def main() -> None:
    consumer = ParcelConsumer()
    await consumer.start()


if __name__ == "__main__":
    asyncio.run(main())
