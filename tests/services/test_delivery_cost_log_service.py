from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest

from app.models import LogData
from app.repositories import DeliveryCostLogRepository
from app.schemas import ParcelType
from app.services import DeliveryCostLogService


def log_factory(parcel_id: int, parcel_type: ParcelType, delivery_cost: Decimal):
    log_data = LogData(
        parcel_id=parcel_id,
        parcel_type=parcel_type,
        delivery_cost=delivery_cost,
        calculated_at=datetime(year=2026, month=9, day=9),
    )

    return log_data


class TestDeliveryCostLogService:
    @pytest.mark.asyncio
    async def test_get_summary(self, get_test_delivery_cost_logs_collection):
        repo = DeliveryCostLogRepository(get_test_delivery_cost_logs_collection)
        service = DeliveryCostLogService(repo)
        expected_sum = Decimal(0)
        for i in range(10):
            test_log_data = log_factory(i, ParcelType.ELECTRONICS, Decimal(str(i)))
            expected_sum += Decimal(str(i))
            await service.create_log(test_log_data)

        assert (
            await service.get_summary(datetime(year=2026, month=9, day=9), ParcelType.ELECTRONICS)
            == expected_sum
        )

    @pytest.mark.asyncio
    async def get_summary_empty_logs(self, get_test_delivery_cost_logs_collection):
        repo = DeliveryCostLogRepository(get_test_delivery_cost_logs_collection)
        service = DeliveryCostLogService(repo)
        expected_sum = Decimal(0)
        for i in range(10):
            test_log_data = log_factory(i, ParcelType.CLOTHES, Decimal(str(i)))
            expected_sum += Decimal(str(i))
            await service.create_log(test_log_data)
        target_date = date.today() - timedelta(days=3)
        assert await service.get_summary(
            target_date=target_date, parcel_type=ParcelType.CLOTHES
        ) == Decimal(0)
