from decimal import Decimal
import httpx
from app.cache.redis import redis
from app.clients.cbr import CBRClient


class ExchangeRateService:

    @staticmethod
    async def get_usd_rub_rate(client: httpx.AsyncClient) -> Decimal:
        rate = await redis.get("exchange_rate:USD_RUB")
        if rate is not None:
            return Decimal(rate.decode("utf-8"))
        rate = await CBRClient.get_usd_rub_rate(client)
        REDIS_KEY = "exchange_rate:USD_RUB"
        await redis.set(REDIS_KEY, str(rate), ex=300) # 5 минут
        return rate
