from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class ParcelCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., max_length=300, description="Название посылки")
    weight: Decimal = Field(..., gt=0, description="Вес посылки в кг")
    parcel_price_usd: Decimal = Field(
        ..., ge=0, description="Стоимость содержимого в долларах"
    )
    type_id: int = Field(..., description="ID типа посылки (связь parcel_types)")


class ParcelCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class ParcelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    weight: Decimal
    parcel_price_usd: Decimal
    delivery_price_rub: Decimal | None
    type_name: str
    created_at: datetime
    updated_at: datetime
