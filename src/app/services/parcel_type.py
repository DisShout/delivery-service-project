from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.parcel_type import ParcelTypeRepository


class ParcelTypeService:
    def __init__(self, db: AsyncSession):
        self.repo = ParcelTypeRepository(db)

    async def get_all(self):
        return await self.repo.get_all()
