"""ORM-модель посылки."""

from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.parcel_type import ParcelType


class Parcel(Base):
    """ORM-представление посылки пользователя и рассчитанной стоимости доставки."""

    __tablename__ = "parcels"
    __table_args__ = (
        CheckConstraint("weight > 0"),
        CheckConstraint("content_cost_usd >= 0"),
        CheckConstraint("delivery_cost_rub >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    weight: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=3))
    type_id: Mapped[int] = mapped_column(ForeignKey("parcel_types.id"))
    content_cost_usd: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2))
    delivery_cost_rub: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=2), nullable=True
    )

    type: Mapped["ParcelType"] = relationship()
