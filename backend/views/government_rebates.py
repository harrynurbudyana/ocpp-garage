from datetime import date
from typing import List

from pydantic import BaseModel

from views import PaginationView


class CreateGovernmentRebateView(BaseModel):
    value: float
    month: int
    year: int


class UpdateGovernmentRebateView(BaseModel):
    value: float


class ReadGovernmentRebateView(BaseModel):
    id: str
    period: date
    value: float

    class Config:
        orm_mode = True


class RebatesPeriodView(BaseModel):
    period: date

    class Config:
        orm_mode = True


class PaginatedGovernmentRebatesView(BaseModel):
    items: List[ReadGovernmentRebateView]
    pagination: PaginationView
