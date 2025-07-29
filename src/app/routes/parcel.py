from fastapi import APIRouter, Request, Depends
from src.app.core.database import get_db
from src.app.services.parcel import ParcelService
from src.app.schemas.parcel import ParcelCreate, ParcelCreateResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/parcels", tags=["Parcels"])


@router.post("/")
async def create_parcel(
    request: Request, data: ParcelCreate, db: AsyncSession = Depends(get_db)
) -> ParcelCreateResponse:
    session_id = request.state.session_id
    return await ParcelService(db).create(data=data, session_id=session_id)
