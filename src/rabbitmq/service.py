import json
import uuid
from src.app.core.database import get_session_context
from src.app.services.parcel import ParcelService
from src.app.schemas.parcel import ParcelCreate
from src.rabbitmq.producer import RabbitMQProducer


class RabbitService:
    """Сервис для интеграции с RabbitMQ."""

    def __init__(self):
        self.producer = RabbitMQProducer()

    async def send_message_to_rabbit(
        self, message: ParcelCreate, session_id: str, parcel_id: uuid.UUID
    ):
        async with self.producer as producer:
            await producer.setup()

            payload = {
                "session_id": session_id,
                "parcel_id": str(parcel_id),
                "parcel": message.model_dump(),
            }

            body = json.dumps(payload).encode("utf-8")

            await producer.send(body)

    async def process_message(self, message: dict):
        """Обрабатывает сообщение из RabbitMQ.
        Сохраняет посылку в базе и рассчитывает стоимость доставки."""
        session_id = message["session_id"]
        parcel_id = uuid.UUID(message["parcel_id"])
        parcel = message["parcel"]

        async with get_session_context() as db:
            service = ParcelService(db)
            await service.calculate_delivery_price_and_create_parcel(
                parcel, session_id, parcel_id
            )
