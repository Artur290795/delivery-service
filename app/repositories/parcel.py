from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Parcel

class ParcelRepository:
    
    @staticmethod
    async def create(session: AsyncSession, parcel_data: dict):
        parcel = Parcel(
            session_id=parcel_data["session_id"],
            name=parcel_data["name"],
            weight=parcel_data["weight"],
            type_id=parcel_data["type_id"],
            content_cost_usd=parcel_data["content_cost_usd"]
        )
        session.add(parcel)
        await session.flush()
        return parcel