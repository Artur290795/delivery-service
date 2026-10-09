"""Модель данных записи журнала расчёта доставки."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class LogData:
    """Данные одной записи журнала расчёта стоимости доставки."""

    parcel_id: int
    parcel_type: str
    delivery_cost: Decimal
    calculated_at: datetime
