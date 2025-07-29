from fastapi import APIRouter, Depends
from src.app.services.parcel_type import ParcelTypeService
from src.app.schemas.parcel_type import ParcelTypeResponse
from src.app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/parcel_types", tags=["ParcelType"])


@router.get("/")
async def get_all(db: AsyncSession = Depends(get_db)) -> list[ParcelTypeResponse]:
    return await ParcelTypeService(db).get_all()
