from decimal import ROUND_HALF_UP, Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.parcel import Parcel
from src.app.services.currency_service import CurrencyService
from src.app.repositories.parcel import ParcelRepository
from src.app.schemas.parcel import (
    ParcelCreateDB,
    ParcelFilter,
    ParcelRead,
    ParcelReadByID,
)
import uuid


class ParcelService:
    """Сервис для работы с посылками: создание, получение, расчёт стоимости."""

    def __init__(self, db: AsyncSession):
        self.repo = ParcelRepository(db)
        self.currency_service = CurrencyService()

    async def create(
        self, data: ParcelCreateDB, session_id: str, parcel_id: uuid.UUID
    ) -> Parcel:
        """Создаёт новую посылку в базе."""
        return await self.repo.create(
            data=data, session_id=session_id, parcel_id=parcel_id
        )

    async def get_parcels_by_session_id(
        self, session_id: str, filters: ParcelFilter
    ) -> list[ParcelRead]:
        """Получает список посылок для текущей сессии с фильтрацией и пагинацией."""
        parcels = await self.repo.get_parecels_by_session_id(
            session_id=session_id, filters=filters
        )
        return [
            ParcelRead.model_validate(
                {
                    "id": p.id,
                    "name": p.name,
                    "weight": p.weight,
                    "parcel_price_usd": p.parcel_price_usd,
                    "delivery_price_rub": p.delivery_price_rub,
                    "created_at": p.created_at,
                    "updated_at": p.updated_at,
                    "type_name": p.type.name if p.type else "Неизвестно",
                }
            )
            for p in parcels
        ]

    async def get_by_id(
        self, session_id: str, parcel_id: uuid.UUID
    ) -> ParcelReadByID | None:
        """Получает данные о посылке по её ID."""
        parcel = await self.repo.get_by_id(parcel_id=parcel_id, session_id=session_id)
        if not parcel:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "По данному id посылка не найдена"
            )

        return ParcelReadByID.model_validate(
            {
                "name": parcel.name,
                "weight": parcel.weight,
                "parcel_price_usd": parcel.parcel_price_usd,
                "delivery_price_rub": parcel.delivery_price_rub,
                "type_name": parcel.type.name if parcel.type else "Неизвестно",
            }
        )

    async def calculate_delivery_price_and_create_parcel(
        self, parcel: dict, session_id: str, parcel_id: uuid.UUID
    ):
        """Рассчитывает стоимость доставки и сохраняет посылку в базу"""
        usd_to_rub = await self.currency_service.get_usd_to_rub()
        usd_to_rub_decimal = Decimal(str(usd_to_rub))

        base_cost = Decimal(parcel["weight"]) * Decimal("0.5") + Decimal(
            parcel["parcel_price_usd"]
        ) * Decimal("0.01")
        delivery_price = (base_cost * usd_to_rub_decimal).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        parcel["delivery_price_rub"] = delivery_price

        parcel = ParcelCreateDB.model_validate(parcel)
        await self.create(parcel, session_id, parcel_id)
