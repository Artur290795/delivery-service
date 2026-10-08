"""Репозиторий типов посылок в PostgreSQL."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ParcelType


class ParcelTypeRepository:
    """Репозиторий доступа к справочнику типов посылок."""
    
    @staticmethod
    async def get_by_name(session: AsyncSession, name: str):
        stmt = select(ParcelType).where(ParcelType.name==name)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[ParcelType]:
        stmt = select(ParcelType)
        result = await session.execute(stmt)
        return result.scalars().all()
