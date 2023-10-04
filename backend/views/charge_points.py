from __future__ import annotations

from datetime import datetime
from typing import List, Dict

from ocpp.v16.enums import ChargePointStatus
from pydantic import BaseModel

from views import PaginationView


class ConnectorView(BaseModel):
    status: ChargePointStatus


class ChargePointUpdateStatusView(BaseModel):
    status: ChargePointStatus
    connectors: Dict | None = None


class CreateChargPointView(BaseModel):
    id: str
    description: str | None = None
    manufacturer: str
    serial_number: str
    model: str
    location: str | None = None


class UpdateChargPointView(BaseModel):
    driver_id: str | None = None
    description: str | None = None
    location: str | None = None
    status: ChargePointStatus | None = None


class ChargePointView(BaseModel):
    id: str
    description: str | None = None
    status: ChargePointStatus
    model: str
    manufacturer: str
    location: str | None = None
    updated_at: datetime | None = None
    connectors: Dict

    class Config:
        orm_mode = True


class SimpleChargePoint(BaseModel):
    id: str
    status: ChargePointStatus
    location: str | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class PaginatedChargePointsView(BaseModel):
    items: List[SimpleChargePoint]
    pagination: PaginationView
