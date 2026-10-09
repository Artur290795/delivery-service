from decimal import Decimal

import pytest

from app.services import ExchangeRateService


class FakeCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        self.store[key] = value


class FakeRateProvider:
    def __init__(self):
        self.called = False

    async def get_usd_rub_rate(self):
        self.called = True
        return Decimal("80.50")


@pytest.mark.asyncio
async def test_get_rate_from_provider():
    cache = FakeCache()
    rate_provider = FakeRateProvider()

    result = await ExchangeRateService.get_usd_rub_rate(
        cache=cache,
        rate_provider=rate_provider,
    )

    assert result == Decimal("80.50")
    assert cache.store["exchange_rate:USD_RUB"] == "80.50"
    assert rate_provider.called


@pytest.mark.asyncio
async def test_get_rate_from_cache():
    cache = FakeCache()
    cache.store["exchange_rate:USD_RUB"] = b"80.50"

    rate_provider = FakeRateProvider()

    result = await ExchangeRateService.get_usd_rub_rate(
        cache=cache,
        rate_provider=rate_provider,
    )

    assert result == Decimal("80.50")
    assert not rate_provider.called
