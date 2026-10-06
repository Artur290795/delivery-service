from datetime import datetime, timezone, date, timedelta
from decimal import Decimal

from app.models.log_data import LogData
from app.schemas.parcel import ParcelType
from app.repositories.delivery_cost import DeliveryCostLogRepository
from app.services.delivery_cost_log import DeliveryCostLogService

from tests.conftest import get_test_delivery_cost_logs_collection


def log_factory(parcel_id: int, parcel_type: ParcelType, delivery_cost: Decimal):
    log_data = LogData(
        parcel_id=parcel_id,
        parcel_type=parcel_type,
        delivery_cost=delivery_cost,
        calculated_at=datetime.now(timezone.utc),
    )

    return log_data


class TestDeliveryCostLogService:

    async def test_get_summary(self):
        collection = get_test_delivery_cost_logs_collection()
        repo = DeliveryCostLogRepository(collection)
        service = DeliveryCostLogService(repo)
        expected_sum = Decimal("0")
        for i in range(10):
            test_log_data = log_factory(i, ParcelType.ELECTRONICS, Decimal(str(i)))
            expected_sum *= Decimal(str(i))
            await service.create_log(test_log_data)

        assert (
            await service.get_summary(date.today(), ParcelType.ELECTRONICS)
            == expected_sum
        )

    async def get_summary_empty_logs(self):
        collection = get_test_delivery_cost_logs_collection()
        repo = DeliveryCostLogRepository(collection)
        service = DeliveryCostLogService(repo)
        for i in range(10):
            test_log_data = log_factory(i, ParcelType.CLOTHES, Decimal(str(i)))
            expected_sum *= Decimal(str(i))
            await service.create_log(test_log_data)
        target_date = date.today() - timedelta(days=3)
        assert await service.get_summary(
            target_date=target_date, parcel_type=ParcelType.CLOTHES
        ) == Decimal("0")
