"""Экспорт репозиториев для доступа к данным."""

from app.repositories.delivery_cost import DeliveryCostLogRepository
from app.repositories.parcel import ParcelRepository
from app.repositories.parcel_type import ParcelTypeRepository

__all__ = [
    "DeliveryCostLogRepository",
    "ParcelRepository",
    "ParcelTypeRepository",
]
