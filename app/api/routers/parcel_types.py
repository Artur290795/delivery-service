"""Маршруты для получения доступных типов посылок."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session
from app.services import ParcelTypeService

router = APIRouter()


@router.get("/parcel-types")
async def get_parcel_types(session: AsyncSession = Depends(get_session)):
    parcel_types = await ParcelTypeService.get_all(session)
    return parcel_types
