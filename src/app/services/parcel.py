from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.parcel import ParcelRepository
from src.app.schemas.parcel import ParcelCreate


class ParcelService:
    def __init__(self, db: AsyncSession):
        self.repo = ParcelRepository(db)

    async def create(self, data: ParcelCreate, session_id: str):
        return await self.repo.create(data=data, session_id=session_id)
