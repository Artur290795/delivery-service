"""Протоколы для кэша и поставщика валютного курса."""

from decimal import Decimal
from typing import Protocol


class Cache(Protocol):
    """Интерфейс асинхронного кэша, используемого сервисами."""

    async def get(self, key: str) -> bytes | None: ...

    async def set(self, key: str, value: str, ex: int | None = None) -> None: ...


class RateProvider(Protocol):
    """Интерфейс поставщика валютного курса."""

    async def get_usd_rub_rate(self) -> Decimal: ...
