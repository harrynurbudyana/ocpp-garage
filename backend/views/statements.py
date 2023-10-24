from datetime import time, datetime
from typing import List, Optional

from pydantic import BaseModel


class TransactionsHourlyPeriod(BaseModel):
    """
    Explication by hours.
    """
    start: Optional[time]
    end: Optional[time]
    rate: float = 0.0
    nordpool_price: float = 0.0
    grid_cost: float = 0.0
    government_rebate: float = 0.0
    total_cost: float = 0.0
    total_consumed: float = 0.0
    per_kw_cost: float = 0.0


class StatementsTransaction(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]
    nordpool_price: float = 0.0
    grid_cost: float = 0.0
    government_rebate: float = 0.0
    total_cost: float = 0.0
    per_kw_cost: float = 0.0
    hours: List[TransactionsHourlyPeriod]


class DriversStatement(BaseModel):
    month: str
    year: int
    total_kw: float
    total_cost: float
    per_kw_cost: float
    name: str
    email: str
    garage_address: str
    transactions: List[StatementsTransaction]
