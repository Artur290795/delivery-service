from decimal import Decimal

import pytest

from app.services import DeliveryCostService


@pytest.mark.parametrize(
    "weight, content_cost_usd, usd_rub_rate, expected",
    [
        (
            Decimal(10),
            Decimal(100),
            Decimal(80),
            Decimal(480),
        ),
        (
            Decimal("2.5"),
            Decimal(50),
            Decimal(90),
            Decimal("157.5"),
        ),
        (
            Decimal("0.5"),
            Decimal(1000),
            Decimal(85),
            Decimal("871.25"),
        ),
    ],
)
def test_calculate(weight, content_cost_usd, usd_rub_rate, expected):
    result = DeliveryCostService.calculate(weight, content_cost_usd, usd_rub_rate)

    assert result == expected
