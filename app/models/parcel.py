from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.parcel_type import ParcelType

class Parcel(Base):
    __tablename__ = "parcels"
    __table_args__ = (
        CheckConstraint("weight > 0"),
        CheckConstraint("content_cost_usd >= 0"),
        CheckConstraint("delivery_cost_rub >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    weight: Mapped[float] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("parcel_types.id"))
    content_cost_usd: Mapped[float] = mapped_column()
    delivery_cost_rub: Mapped[float | None] = mapped_column(nullable=True)

    type: Mapped["ParcelType"] = relationship()

