from decimal import Decimal

from app.protocols import RateProvider, Cache

class ExchangeRateService:

    _REDIS_KEY = "exchange_rate:USD_RUB"

    @staticmethod
    async def get_usd_rub_rate(cache: Cache, rate_provider: RateProvider) -> Decimal:
        rate = await cache.get(ExchangeRateService._REDIS_KEY)
        if rate is not None:
            return Decimal(rate.decode("utf-8"))
        rate = await rate_provider.get_usd_rub_rate()
        
        await cache.set(ExchangeRateService._REDIS_KEY, str(rate), ex=300) # 5 минут
        return rate
