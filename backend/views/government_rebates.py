from datetime import datetime
from typing import List

from pydantic import BaseModel

from views import PaginationView


class CreateGovernmentRebateView(BaseModel):
    value: float


class UpdateGovernmentRebateView(BaseModel):
    value: str


class ReadGovernmentRebateView(BaseModel):
    created_at: datetime
    value: float


class PaginatedGovernmentRebatesView(BaseModel):
    items: List[ReadGovernmentRebateView]
    pagination: PaginationView
