from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.fields import TransactionStatus
from views import PaginationView


class CreateTransactionView(BaseModel):
    garage: str
    meter_start: int
    meter_start: int
    charge_point: str
    connector: int
    status: TransactionStatus | None = None


class InitTransactionView(BaseModel):
    charge_point_id: str
    connector_id: int


class UpdateTransactionView(BaseModel):
    meter_stop: int | None = None
    status: TransactionStatus | None = None


class Transaction(BaseModel):
    id: str
    meter_start: int
    meter_stop: int | None = None
    charge_point: str
    connector: int
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class PaginatedTransactionsView(BaseModel):
    items: List[Transaction]
    pagination: PaginationView
