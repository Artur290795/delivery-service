"""Сервис доступа к справочнику типов посылок."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ParcelTypeRepository


class ParcelTypeService:
    """Тип посылки: ORM-модель справочника или значение API-схемы."""

    @staticmethod
    async def get_all(session: AsyncSession):
        parcel_types = await ParcelTypeRepository.get_all(session)
        return parcel_types
