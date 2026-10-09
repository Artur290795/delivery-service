"""Экспорт маршрутизаторов HTTP API."""

from app.api.routers.delivery_costs import router as delivery_costs_router
from app.api.routers.parcel import router as parcel_router
from app.api.routers.parcel_types import router as parcel_types_router
from app.api.routers.support import router as support_router

__all__ = [
    "delivery_costs_router",
    "parcel_router",
    "parcel_types_router",
    "support_router",
]
