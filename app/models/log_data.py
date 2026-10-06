from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.schemas import ParcelType


@dataclass
class LogData:
    parcel_id: int
    parcel_type: ParcelType
    delivery_cost: Decimal
    calculated_at: datetime
