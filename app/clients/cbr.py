from decimal import Decimal
import httpx


CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

class CBRClient:
    
    @staticmethod
    async def get_usd_rub_rate(client: httpx.AsyncClient) -> Decimal:
        response = await client.get(CBR_URL)
        response.raise_for_status()
        data = response.json()
        usd_rub_rate = Decimal(str(data["Valute"]["USD"]["Value"]))
        return usd_rub_rate
