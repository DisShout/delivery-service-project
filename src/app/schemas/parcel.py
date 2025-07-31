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


class ParcelFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type_name: str | None = Field(None, description="Фильтр по имени типа посылки")
    has_delivery_price: bool | None = Field(
        None, description="True - только с ценой, False - только без цены"
    )
    limit: int = Field(10, ge=1, le=100, description="Количество записей на странице")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")


class ParcelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    weight: Decimal
    parcel_price_usd: Decimal
    delivery_price_rub: str | None
    type_name: str
    created_at: datetime
    updated_at: datetime


class ParcelReadByID(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    weight: Decimal
    type_name: str
    parcel_price_usd: Decimal
    delivery_price_rub: str | None
