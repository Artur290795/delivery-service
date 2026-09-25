from unittest.mock import AsyncMock, patch
from decimal import Decimal

import pytest

from app.models.parcel import Parcel
from app.services.delivery_cost import DeliveryCostService
from tests.services.test_exchange_rate import FakeCache, FakeRateProvider


@pytest.mark.parametrize(
    "weight, content_cost_usd, usd_rub_rate, expected",
    [
        (
            Decimal("10"),
            Decimal("100"),
            Decimal("80"),
            Decimal("480"),
        ),
        (
            Decimal("2.5"),
            Decimal("50"),
            Decimal("90"),
            Decimal("157.5"),
        ),
        (
            Decimal("0.5"),
            Decimal("1000"),
            Decimal("85"),
            Decimal("871.25"),
        ),
    ],
)
def test_calculate(weight, content_cost_usd, usd_rub_rate, expected):
    result = DeliveryCostService.calculate(weight, content_cost_usd, usd_rub_rate)

    assert result == expected


def make_parcel(
    *,
    weight: Decimal = Decimal("10"),
    content_cost_usd: Decimal = Decimal("100"),
    delivery_cost_rub: Decimal | None = None,
) -> Parcel:
    return Parcel(
        weight=weight,
        content_cost_usd=content_cost_usd,
        delivery_cost_rub=delivery_cost_rub,
    )

@pytest.mark.asyncio
async def test_calculate_delivery_costs():
    session = AsyncMock()
    fake_cache = FakeCache()
    fake_provider = FakeRateProvider()

    with patch("app.services.delivery_cost.ParcelRepository.get_unprocessed_parcels") as mock:
        parcel1 = make_parcel()
        parcel2 = make_parcel(
            weight=Decimal("2.5"),
            content_cost_usd=Decimal("50"),
        )
        mock.return_value = [parcel1, parcel2]
        await DeliveryCostService.calculate_delivery_costs(
            cache=fake_cache,
            rate_provider=fake_provider,
            session=session,
        )
        assert parcel1.delivery_cost_rub == Decimal("483.00")
        assert parcel2.delivery_cost_rub == Decimal("140.88")
        session.commit.assert_awaited_once()
