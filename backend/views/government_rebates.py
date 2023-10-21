from datetime import datetime
from typing import List

from pydantic import BaseModel

from views import PaginationView


class CreateGovernmentRebateView(BaseModel):
    value: float


class UpdateGovernmentRebateView(BaseModel):
    value: float


class ReadGovernmentRebateView(BaseModel):
    id: str
    created_at: datetime
    value: float

    class Config:
        orm_mode = True


class PaginatedGovernmentRebatesView(BaseModel):
    items: List[ReadGovernmentRebateView]
    pagination: PaginationView
