from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from src.app.core.database import Base


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    parcels: Mapped[list["Parcel"]] = relationship(back_populates="type")  # pyright: ignore[reportUndefinedVariable] # noqa: F821
