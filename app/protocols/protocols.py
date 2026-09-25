from typing import Protocol
from decimal import Decimal


class Cache(Protocol):
    async def get(self, key: str) -> bytes | None: ...

    async def set(self, key: str, value: str, ex: int | None = None) -> None: ...


class RateProvider(Protocol):
    async def get_usd_rub_rate(self) -> Decimal: ...
