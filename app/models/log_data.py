from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class LogData:
    parcel_id: int
    parcel_type: str
    delivery_cost: Decimal
    calculated_at: datetime
