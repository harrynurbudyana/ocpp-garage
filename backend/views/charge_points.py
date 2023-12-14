from __future__ import annotations

from datetime import datetime
from typing import List

from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
from pydantic import BaseModel

from views import PaginationView


class CreateChargPointView(BaseModel):
    id: str
    description: str | None = None
    vendor: str | None = None
    serial_number: str | None = None
    model: str | None = None
    location: str | None = None


class UpdateChargPointView(BaseModel):
    description: str | None = None
    location: str | None = None
    status: ChargePointStatus | None = None
    error_code: ChargePointErrorCode | None = None
    latest_limit: int | None = None


class ChargePointView(BaseModel):
    id: str
    description: str | None = None
    status: ChargePointStatus
    model: str | None = None
    vendor: str | None = None
    connectors: List[SimpleConnectorView] = []

    class Config:
        orm_mode = True


class SimpleChargePoint(BaseModel):
    id: str
    status: ChargePointStatus
    location: str | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class SimpleConnectorView(BaseModel):
    id: int
    status: ChargePointStatus
    error_code: ChargePointErrorCode

    class Config:
        orm_mode = True


class ConnectorView(BaseModel):
    id: int
    status: ChargePointStatus
    error_code: ChargePointErrorCode
    charge_point: SimpleChargePoint

    class Config:
        orm_mode = True


ConnectorView.update_forward_refs()
ChargePointView.update_forward_refs()


class PaginatedChargePointsView(BaseModel):
    items: List[SimpleChargePoint]
    pagination: PaginationView
