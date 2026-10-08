"""Сервис получения и кэширования курса USD/RUB."""

from decimal import Decimal

from loguru import logger

from app.protocols import RateProvider, Cache
from app.config import settings

class ExchangeRateService:
    """Сервис кэшированного получения курса USD/RUB."""

    _REDIS_KEY = "exchange_rate:USD_RUB"

    @staticmethod
    async def get_usd_rub_rate(cache: Cache, rate_provider: RateProvider) -> Decimal:
        rate = await cache.get(ExchangeRateService._REDIS_KEY)
        if rate is not None:
            logger.debug("USD/RUB rate retrieved from cache")
            return Decimal(rate.decode("utf-8"))
        rate = await rate_provider.get_usd_rub_rate()
        logger.info("USD/RUB rate retrieved from provider")
        
        await cache.set(
            ExchangeRateService._REDIS_KEY,
            str(rate),
            ex=settings.exchange_rate_cache_ttl_seconds,
        )
        return rate
