import asyncio
import json
from aio_pika import IncomingMessage
from src.rabbitmq.service import RabbitService
from src.rabbitmq.base import BaseRabbitMQClient
from src.app.core.config import get_settings

settings = get_settings()
print(">>> Consumer DB_URL:", settings.DATABASE_URL)


class RabbitMQConsumer(BaseRabbitMQClient):
    """Слушатель очереди RabbitMQ с использованием базового клиента."""

    def __init__(self):
        super().__init__()
        self.rabbit_service = RabbitService()
        self.rabbit_topic = "parcel"

    async def start(self):
        """Запуск слушателя RabbitMQ."""
        await self.connect()
        async with self.connection:
            async with self.channel:
                queue = await self._declare_or_get_queue(self.channel)
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            await self.handle_message(message)

    async def _declare_or_get_queue(self, channel):
        """Объявляет очередь и обменник, затем биндит их."""
        exchange = await channel.declare_exchange(
            self.rabbit_topic,  # "parcel"
            type="direct",  # можно fanout или topic, зависит от логики
            durable=True,
        )

        queue = await channel.declare_queue(
            self.rabbit_topic, durable=True, arguments={"x-queue-type": "quorum"}
        )

        await queue.bind(exchange=exchange, routing_key=self.rabbit_topic)
        return queue

    async def handle_message(self, message: IncomingMessage):
        msg_data = json.loads(message.body.decode())

        await self.rabbit_service.process_message(msg_data)


if __name__ == "__main__":
    consumer = RabbitMQConsumer()

    asyncio.run(consumer.start())
