from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.app.core.database import Base


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)