from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.parcel import ParcelType


class DeliveryCostSummaryResponse(BaseModel):
    target_date: date
    parcel_type: ParcelType
    total_delivery_cost: Decimal
