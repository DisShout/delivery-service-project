import uuid
from fastapi import APIRouter, Request, Depends
from src.rabbitmq.service import RabbitService
from src.app.core.database import get_db
from src.app.services.parcel import ParcelService
from src.app.schemas.parcel import (
    ParcelCreate,
    ParcelCreateResponse,
    ParcelFilter,
    ParcelRead,
    ParcelReadByID,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/parcels", tags=["Parcels"])


@router.post("/")
async def create_parcel(request: Request, data: ParcelCreate) -> ParcelCreateResponse:
    session_id = request.state.session_id
    parcel_id = uuid.uuid4()
    await RabbitService().send_message_to_rabbit(
        message=data, session_id=session_id, parcel_id=parcel_id
    )
    return ParcelCreateResponse(id=parcel_id, name=data.name)


@router.get("/", response_model=list[ParcelRead])
async def get_parcels_by_session_id(
    request: Request,
    filters: ParcelFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = ParcelService(db)
    return await service.get_parcels_by_session_id(
        session_id=request.state.session_id, filters=filters
    )


@router.get("/{parcel_id}", response_model=ParcelReadByID)
async def get_by_id(
    parcel_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = ParcelService(db)
    parcel = await service.get_by_id(
        session_id=request.state.session_id, parcel_id=parcel_id
    )
    return parcel
