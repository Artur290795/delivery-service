from datetime import date

from fastapi import APIRouter, Depends

from app.services.delivery_cost_log import DeliveryCostLogService
from app.api.dependencies import get_delivery_cost_log_service
from app.schemas.parcel import ParcelType, DeliveryCostSummaryResponse

router = APIRouter()


@router.get("/delivery-cost/logs/summary")
async def get_delivery_cost_logs_summary(
    target_date: date,
    parcel_type: ParcelType,
    service: DeliveryCostLogService = Depends(get_delivery_cost_log_service),
) -> DeliveryCostSummaryResponse:
    delivery_cost_summary = await service.get_summary(target_date, parcel_type)
    return DeliveryCostSummaryResponse(
        target_date=target_date,
        parcel_type=parcel_type,
        total_delivery_cost=delivery_cost_summary,
    )
