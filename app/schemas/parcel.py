from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class ParcelType(str, Enum):
    CLOTHES = "clothes"
    ELECTRONICS = "electronics"
    OTHER = "other"


class ParcelCreate(BaseModel):
    name: str = Field(min_length=1)
    weight: Decimal = Field(gt=0)
    type: ParcelType
    content_cost_usd: Decimal = Field(ge=0)


class ParcelCreateResponse(BaseModel):
    status: str
    task_id: str


class ParcelResponse(BaseModel):
    id: int
    name: str
    weight: Decimal
    type: ParcelType
    content_cost_usd: Decimal
    delivery_cost_rub: Decimal | str
