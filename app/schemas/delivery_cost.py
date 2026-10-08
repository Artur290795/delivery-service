"""Схемы ответов для аналитики стоимости доставки."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.parcel import ParcelType


class DeliveryCostSummaryResponse(BaseModel):
    """Агрегированная стоимость доставок по дате и типу посылки."""
    target_date: date
    parcel_type: ParcelType
    total_delivery_cost: Decimal
