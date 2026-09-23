from decimal import Decimal, ROUND_HALF_UP

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.parcel import ParcelRepository
from app.services.exchange_rate import ExchangeRateService

class DeliveryCostService:
    @staticmethod
    def calculate(weight: Decimal, content_cost_usd: Decimal, usd_rub_rate: Decimal) -> Decimal:
        result = (
            weight * Decimal("0.5") + content_cost_usd * Decimal("0.01")
        ) * usd_rub_rate
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


    @staticmethod
    async def calculate_delivery_costs(client: httpx.AsyncClient, session: AsyncSession) -> None:
        unprocessed_parcels = await ParcelRepository.get_unprocessed_parcels(session)
        rate = await ExchangeRateService.get_usd_rub_rate(client)
        try:
            for parcel in unprocessed_parcels:
                delivery_cost = DeliveryCostService.calculate(
                    parcel.weight, parcel.content_cost_usd, rate
                )
                parcel.delivery_cost_rub = delivery_cost
            await session.commit()
        except Exception:
            await session.rollback()
            raise
