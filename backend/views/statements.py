from datetime import time, datetime
from typing import List

from pydantic import BaseModel, validator

from views import PaginationView


class TransactionView(BaseModel):
    start: time
    end: time
    nordpool_price: float = 0.0
    grid_cost: float = 0.0
    government_rebate: float = 0.0
    total_cost: float = 0.0
    per_kw_cost: float = 0.0

    @validator("nordpool_price", always=True)
    def format_nordpool_price(cls, value, values, config, field):
        return round(value, 2)

    @validator("grid_cost", always=True)
    def format_grid_cost(cls, value, values, config, field):
        return round(value, 2)

    @validator("government_rebate", always=True)
    def format_government_rebate(cls, value, values, config, field):
        return round(value, 2)

    @validator("total_cost", always=True)
    def format_total_cost(cls, value, values, config, field):
        return round(value, 2)

    @validator("per_kw_cost", always=True)
    def format_per_kw_cost(cls, value, values, config, field):
        return round(value, 2)


class TransactionsHourlyPeriod(TransactionView):
    """
    Explication by hours.
    """
    total_consumed: float = 0.0

    @validator("total_consumed", always=True)
    def format_total_consumed(cls, value, values, config, field):
        return round(value, 2)


class StatementsTransaction(TransactionView):
    start: datetime
    end: datetime
    per_kw_cost: float = 0.0
    hours: List[TransactionsHourlyPeriod]

    @validator("per_kw_cost", always=True)
    def format_per_kw_cost(cls, value, values, config, field):
        return round(value, 2)


class DriversStatement(BaseModel):
    payment_link: str | None = None
    month: str
    year: int
    total_kw: float
    total_cost: float
    per_kw_cost: float
    name: str
    email: str
    garage_address: str
    transactions: List[StatementsTransaction]

    @validator("per_kw_cost", always=True)
    def format_per_kw_cost(cls, value, values, config, field):
        return round(value, 2)


class StatementView(BaseModel):
    month: int
    year: int
    sum: float
    is_active: bool

    class Config:
        orm_mode = True


class PaginatedStatementsView(BaseModel):
    items: List[StatementView]
    pagination: PaginationView