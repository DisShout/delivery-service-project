from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, ForeignKey, DateTime, func
from src.app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from decimal import Decimal


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    parcel_price_usd: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    delivery_price_rub: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), nullable=True
    )
    type_id: Mapped[int] = mapped_column(ForeignKey("parcel_types.id"), nullable=False)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    type: Mapped["ParcelType"] = relationship(back_populates="parcels")  # pyright: ignore[reportUndefinedVariable]  # noqa: F821

    def __repr__(self):
        return f"<Parcel(id={self.id}, name={self.name}, weight={self.weight}, type_id={self.type_id})>"
