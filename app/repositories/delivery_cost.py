"""Репозиторий журнала расчётов доставки в MongoDB."""

from bson import Decimal128
from datetime import date, datetime, timedelta

from app.models import LogData


class DeliveryCostLogRepository:
    """Репозиторий записей журнала стоимости доставки."""
    def __init__(self, collection):
        self.collection = collection

    async def create_log(self, log_data: LogData):
        await self.collection.insert_one(
            {
                "parcel_id": log_data.parcel_id,
                "parcel_type": log_data.parcel_type,
                "delivery_cost": Decimal128(str(log_data.delivery_cost)),
                "calculated_at": log_data.calculated_at,
            }
        )

    async def get_logs_by_date_and_type(
        self, date: date, parcel_type: str
    ) -> list[LogData]:
        start_of_day = datetime.combine(date, datetime.min.time())
        next_day = start_of_day + timedelta(days=1)
        pipeline = [
            {
                "$match": {
                    "parcel_type": parcel_type,
                    "calculated_at": {
                        "$gte": start_of_day,
                        "$lt": next_day,
                    },
                }
            }
        ]

        cursor = await self.collection.aggregate(pipeline)

        raw_result = await cursor.to_list(length=None)

        result = [
            LogData(
                doc["parcel_id"],
                doc["parcel_type"],
                doc["delivery_cost"].to_decimal(),
                doc["calculated_at"],
            )
            for doc in raw_result
        ]

        return result
