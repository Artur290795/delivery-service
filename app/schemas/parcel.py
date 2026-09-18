from enum import Enum

from pydantic import BaseModel, Field

class ParcelType(str, Enum):
    CLOTHES = "clothes"
    ELECTRONICS = "electronics"
    OTHER = "other"

class ParcelCreate(BaseModel):
    name: str = Field(min_length=1)
    weight: float = Field(gt=0)
    type: ParcelType
    content_cost_usd: float = Field(ge=0)
