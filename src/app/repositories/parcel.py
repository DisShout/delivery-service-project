from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.parcel_type import ParcelType
from src.app.models.parcel import Parcel
from src.app.schemas.parcel import ParcelCreateDB, ParcelFilter
from sqlalchemy.orm import joinedload
import uuid


class ParcelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ParcelCreateDB, session_id: str) -> Parcel:
        parcel = Parcel(
            name=data.name,
            weight=data.weight,
            parcel_price_usd=data.parcel_price_usd,
            type_id=data.type_id,
            session_id=session_id,
            delivery_price_rub=data.delivery_price_rub,
        )
        self.db.add(parcel)
        await self.db.commit()
        await self.db.refresh(parcel)
        return parcel

    async def get_parecels_by_session_id(
        self, session_id: str, filters: ParcelFilter
    ) -> list[Parcel]:
        query = (
            select(Parcel)
            .join(Parcel.type)
            .options(joinedload(Parcel.type))
            .where(Parcel.session_id == session_id)
        )

        if filters.type_name:
            query = query.where(ParcelType.name == filters.type_name)

        if filters.has_delivery_price is not None:
            if filters.has_delivery_price:
                query = query.where(Parcel.delivery_price_rub.isnot(None))
            else:
                query = query.where(Parcel.delivery_price_rub.is_(None))

        query = query.limit(filters.limit).offset(filters.offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, parcel_id: uuid.UUID, session_id: str) -> Parcel | None:
        query = (
            select(Parcel)
            .join(Parcel.type)
            .options(joinedload(Parcel.type))
            .where(Parcel.id == parcel_id, Parcel.session_id == session_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_unpriced_parcels(self) -> list[Parcel]:
        query = (
            select(Parcel)
            .options(joinedload(Parcel.type))
            .where(Parcel.delivery_price_rub.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def save(self, parcel: Parcel) -> Parcel:
        self.db.add(parcel)
        await self.db.commit()
        await self.db.refresh(parcel)
        return parcel
