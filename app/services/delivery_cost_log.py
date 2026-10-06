from datetime import date
from decimal import Decimal

from app.models.log_data import LogData
from app.repositories import DeliveryCostLogRepository
from app.schemas import ParcelType


class DeliveryCostLogService:
    def __init__(self, delivery_cost_log_repo: DeliveryCostLogRepository):
        self.log_data_repository = delivery_cost_log_repo

    async def get_summary(self, target_date: date, parcel_type: ParcelType):
        result = await self.log_data_repository.get_logs_by_date_and_type(
            target_date, parcel_type
        )
        values = [log.delivery_cost for log in result]
        return sum(values, Decimal("0"))

    async def create_log(self, log_data: LogData):
        await self.log_data_repository.create_log(log_data)
