"""HTTP-клиент Центрального банка России для получения курса USD/RUB."""

from decimal import Decimal

import httpx

from app.config import settings


class CBRClient:
    """Клиент HTTP API ЦБ РФ для получения курса доллара."""

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_usd_rub_rate(self) -> Decimal:
        response = await self.client.get(settings.cbr_url)
        response.raise_for_status()
        data = response.json()
        return Decimal(str(data["Valute"]["USD"]["Value"]))
