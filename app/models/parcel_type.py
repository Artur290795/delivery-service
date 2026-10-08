"""ORM-модель типа посылки."""

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ParcelType(Base):
    """Тип посылки: ORM-модель справочника или значение API-схемы."""

    __tablename__ = "parcel_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
