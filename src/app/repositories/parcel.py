from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.parcel import Parcel
from src.app.schemas.parcel import ParcelCreate


class ParcelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ParcelCreate, session_id: str) -> Parcel:
        parcel = Parcel(
            name=data.name,
            weight=data.weight,
            parcel_price_usd=data.parcel_price_usd,
            type_id=data.type_id,
            session_id=session_id,
        )
        self.db.add(parcel)
        await self.db.commit()
        await self.db.refresh(parcel)
        return parcel
