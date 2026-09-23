from sqlalchemy.ext.asyncio import AsyncSession
from app.custom_exceptions import InvalidParcelTypeException
from app.repositories import ParcelRepository, ParcelTypeRepository
from app.schemas.parcel import (
    ParcelCreate,
    ParcelCreateResponse,
    ParcelResponse,
    ParcelType,
)


class ParcelService:

    @staticmethod
    async def create(
        session: AsyncSession,
        parcel_create: ParcelCreate,
        session_id: str,
    ):
        parcel_data = parcel_create.model_dump()
        parcel_data["session_id"] = session_id
        parcel_type = await ParcelTypeRepository.get_by_name(
            session, parcel_create.type.value
        )
        if parcel_type:
            parcel_data["type_id"] = parcel_type.id
            del parcel_data["type"]
            try:
                new_parcel = await ParcelRepository.create(session, parcel_data)
                parcel_id = new_parcel.id
                await session.commit()
                return ParcelCreateResponse(id=parcel_id)
            except Exception:
                await session.rollback()
                raise
        raise InvalidParcelTypeException("Invalid type of parcel")

    @staticmethod
    async def get_user_parcels(
        session: AsyncSession,
        session_id: str,
        limit: int,
        offset: int,
        parcel_type: ParcelType | None = None,
        delivery_cost_calculated: bool | None = None,
    ) -> list[ParcelResponse]:
        parcels = await ParcelRepository.get_user_parcels(
            session,
            session_id,
            limit,
            offset,
            parcel_type.value if parcel_type else None,
            delivery_cost_calculated,
        )

        result = []
        for parcel in parcels:
            parcel_dict = {
                "id": parcel.id,
                "name": parcel.name,
                "weight": parcel.weight,
                "type": parcel.type.name,
                "content_cost_usd": parcel.content_cost_usd,
                "delivery_cost_rub": (
                    parcel.delivery_cost_rub
                    if parcel.delivery_cost_rub is not None
                    else "Стоимость посылки еще не рассчитана"
                ),
            }
            result.append(ParcelResponse(**parcel_dict))
        return result
