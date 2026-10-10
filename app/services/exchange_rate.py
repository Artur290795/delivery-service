"""Сервис получения и кэширования курса USD/RUB."""

from decimal import Decimal

from loguru import logger

from app.config import settings
from app.protocols import Cache, RateProvider


class ExchangeRateService:
    """Сервис кэшированного получения курса USD/RUB."""

    _REDIS_KEY = "exchange_rate:USD_RUB"

    @staticmethod
    async def get_usd_rub_rate(cache: Cache, rate_provider: RateProvider) -> Decimal:
        cached_rate = await cache.get(ExchangeRateService._REDIS_KEY)
        if cached_rate is not None:
            logger.debug("USD/RUB rate retrieved from cache")
            return Decimal(cached_rate.decode("utf-8"))
        rate = await rate_provider.get_usd_rub_rate()
        logger.info("USD/RUB rate retrieved from provider")

        await cache.set(
            ExchangeRateService._REDIS_KEY,
            str(rate),
            ex=settings.exchange_rate_cache_ttl_seconds,
        )
        return rate
