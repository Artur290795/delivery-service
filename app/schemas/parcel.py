"""Схемы запросов и ответов для работы с посылками."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class ParcelType(str, Enum):
    """Тип посылки: ORM-модель справочника или значение API-схемы."""
    CLOTHES = "clothes"
    ELECTRONICS = "electronics"
    OTHER = "other"


class ParcelCreate(BaseModel):
    """ORM-представление посылки пользователя и рассчитанной стоимости доставки."""
    name: str = Field(min_length=1)
    weight: Decimal = Field(gt=0)
    type: ParcelType
    content_cost_usd: Decimal = Field(ge=0)


class ParcelCreateResponse(BaseModel):
    """Ответ API, подтверждающий постановку регистрации в очередь."""
    status: str
    task_id: str


class ParcelResponse(BaseModel):
    """Полное представление посылки в ответах API."""
    id: int
    name: str
    weight: Decimal
    type: ParcelType
    content_cost_usd: Decimal
    delivery_cost_rub: Decimal | str
