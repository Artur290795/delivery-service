from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LogData
from app.protocols import RateProvider, Cache
from app.repositories import ParcelRepository
from app.services.delivery_cost_log import DeliveryCostLogService
from app.services.exchange_rate import ExchangeRateService


class DeliveryCostService:
    
    @staticmethod
    def calculate(
        weight: Decimal, content_cost_usd: Decimal, usd_rub_rate: Decimal
    ) -> Decimal:
        result = (
            weight * Decimal("0.5") + content_cost_usd * Decimal("0.01")
        ) * usd_rub_rate
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    async def calculate_delivery_costs(
        cache: Cache,
        rate_provider: RateProvider,
        session: AsyncSession,
        delivery_cost_log_service: DeliveryCostLogService,
    ) -> None:
        unprocessed_parcels = await ParcelRepository.get_unprocessed_parcels(session)
        rate = await ExchangeRateService.get_usd_rub_rate(
            cache=cache, rate_provider=rate_provider
        )
        try:
            logs = []
            for parcel in unprocessed_parcels:
                delivery_cost = DeliveryCostService.calculate(
                    parcel.weight, parcel.content_cost_usd, rate
                )
                parcel.delivery_cost_rub = delivery_cost
                log_data = LogData(
                    parcel_id=parcel.id,
                    parcel_type=parcel.type.name,
                    delivery_cost=delivery_cost,
                    calculated_at=datetime.now(timezone.utc),
                )
                logs.append(log_data)

            await session.commit()
            for log_data in logs:
                await delivery_cost_log_service.create_log(log_data)

        except Exception:
            await session.rollback()
            raise
