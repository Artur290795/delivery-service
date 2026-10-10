"""Экспорт маршрутизаторов HTTP API."""

from fastapi import APIRouter

from app.api.routers.delivery_costs import router as delivery_costs_router
from app.api.routers.parcel import router as parcel_router
from app.api.routers.parcel_types import router as parcel_types_router
from app.api.routers.support import router as support_router

router = APIRouter(prefix="/api/v1")
router.include_router(parcel_router)
router.include_router(delivery_costs_router)
router.include_router(parcel_types_router)
router.include_router(support_router)


__all__ = ["router"]
