import asyncio
import aio_pika
import logging
from aio_pika import RobustConnection, RobustChannel
from src.app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class BaseRabbitMQClient:
    """Базовый класс для подключения к RabbitMQ с управлением ресурсами через контекстный менеджер."""

    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.connection: RobustConnection = None
        self.channel: RobustChannel = None

    async def connect(self, retries: int = 10, delay: int = 5):
        """Устанавливает соединение и создаёт канал с retry логикой."""
        for attempt in range(1, retries + 1):
            try:
                self.connection = await aio_pika.connect_robust(
                    host=self.host,
                    port=self.port,
                    login=self.user,
                    password=self.password,
                )
                self.channel = await self.connection.channel()
                logger.info("RabbitMQ connected successfully")
                return
            except Exception as e:
                logger.warning(
                    f"[RabbitMQ] Connection attempt {attempt}/{retries} failed: {e}"
                )
                if attempt == retries:
                    logger.error("RabbitMQ connection failed after all retries")
                    raise
                await asyncio.sleep(delay)

    async def close(self):
        """Закрывает соединение с RabbitMQ."""
        if self.connection:
            await self.connection.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
