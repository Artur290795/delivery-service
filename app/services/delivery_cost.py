from decimal import Decimal, ROUND_HALF_UP


class DeliveryCostService:

    @staticmethod
    def calculate(
        weight: Decimal, content_cost_usd: Decimal, usd_rub_rate: Decimal
    ) -> Decimal:
        result = (
            weight * Decimal("0.5") + content_cost_usd * Decimal("0.01")
        ) * usd_rub_rate
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
