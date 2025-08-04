from aio_pika import ExchangeType, Message

from src.rabbitmq.base import BaseRabbitMQClient


class RabbitMQProducer(BaseRabbitMQClient):
    """Продюсер для отправки данных в сервисы с поддержкой контекстного менеджера."""

    def __init__(self):
        super().__init__()
        self.exchange = None

    async def setup(self):
        """Создаёт обменник, если соединение установлено."""
        self.exchange = await self.channel.declare_exchange(
            name="parcel",
            type=ExchangeType.DIRECT,
            durable=True,
        )

    async def send(self, data: bytes, routing_key: str = "parcel"):
        """Отправляет данные по указанному routing_key."""
        if self.exchange is None:
            raise RuntimeError(
                "Exchange не инициализирован. Вызовите setup() перед send()."
            )

        message = Message(body=data, content_type="application/json")
        await self.exchange.publish(message, routing_key=routing_key)
