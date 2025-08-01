from decimal import ROUND_HALF_UP, Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.parcel import Parcel
from src.app.services.currency_service import CurrencyService
from src.app.repositories.parcel import ParcelRepository
from src.app.schemas.parcel import (
    ParcelCreate,
    ParcelFilter,
    ParcelRead,
    ParcelReadByID,
)
import uuid


class ParcelService:
    def __init__(self, db: AsyncSession):
        self.repo = ParcelRepository(db)
        self.currency_service = CurrencyService()

    async def create(self, data: ParcelCreate, session_id: str) -> Parcel:
        return await self.repo.create(data=data, session_id=session_id)

    async def get_parcels_by_session_id(
        self, session_id: str, filters: ParcelFilter
    ) -> list[ParcelRead]:
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
                    "delivery_price_rub": str(p.delivery_price_rub)
                    if p.delivery_price_rub is not None
                    else "Не рассчитано",
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
                "delivery_price_rub": str(parcel.delivery_price_rub)
                if parcel.delivery_price_rub is not None
                else "Не рассчитано",
                "type_name": parcel.type.name if parcel.type else "Неизвестно",
            }
        )

    async def calculate_delivery_price(self, parcel: Parcel) -> Decimal:
        usd_to_rub = await self.currency_service.get_usd_to_rub()
        base_cost = parcel.weight * Decimal("0.5") + parcel.parcel_price_usd * Decimal(
            "0.01"
        )
        delivery_price = base_cost * usd_to_rub
        return delivery_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    async def update_delivery_price(self, parcel: Parcel) -> Parcel:
        parcel.delivery_price_rub = await self.calculate_delivery_price(parcel)
        return await self.repo.save(parcel)

    async def update_all_unpriced(self) -> list[Parcel]:
        parcels = await self.repo.get_unpriced_parcels()
        updated = []
        for parcel in parcels:
            updated_parcel = await self.update_delivery_price(parcel)
            updated.append(updated_parcel)
        return updated
