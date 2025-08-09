from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.parcel_type import ParcelType
from sqlalchemy import select


class ParcelTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> ParcelType:
        results = await self.db.execute(select(ParcelType))
        return results.scalars().all()
