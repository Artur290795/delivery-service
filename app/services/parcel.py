from sqlalchemy.ext.asyncio import AsyncSession
from app.custom_exceptions import InvalidParcelTypeException
from app.repositories import ParcelRepository, ParcelTypeRepository
from app.schemas.parcel import ParcelCreate, ParcelType


class ParcelService:
    
    @staticmethod
    async def create(session: AsyncSession, parcel_create: ParcelCreate):
        parcel_data = parcel_create.model_dump()
        parcel_type = await ParcelTypeRepository.get_by_name(
            session, parcel_create.type.value
        )
        if parcel_type:
            parcel_data["type_id"] = parcel_type.id
            del parcel_data["type"]
            try:
                new_parcel = await ParcelRepository.create(session, parcel_data)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            return new_parcel
        raise InvalidParcelTypeException("Invalid type of parcel")
