from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models import Parcel, ParcelType


class ParcelRepository:

    @staticmethod
    async def create(session: AsyncSession, parcel_data: dict):
        parcel = Parcel(
            session_id=parcel_data["session_id"],
            name=parcel_data["name"],
            weight=parcel_data["weight"],
            type_id=parcel_data["type_id"],
            content_cost_usd=parcel_data["content_cost_usd"],
        )
        session.add(parcel)
        await session.flush()
        return parcel

    @staticmethod
    async def get_user_parcels(
        session: AsyncSession,
        session_id: str,
        limit: int,
        offset: int,
        parcel_type: str | None = None,
        delivery_cost_calculated: bool | None = None,
    ):
        stmt = (
            select(Parcel)
            .options(selectinload(Parcel.type))
            .join(Parcel.type)
            .where(Parcel.session_id == session_id)
        )
        if parcel_type is not None:
            stmt = stmt.where(ParcelType.name == parcel_type)
        if delivery_cost_calculated is not None:
            if delivery_cost_calculated:
                stmt = stmt.where(Parcel.delivery_cost_rub.is_not(None))
            else:
                stmt = stmt.where(Parcel.delivery_cost_rub.is_(None))
        stmt = stmt.limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.scalars().all()
