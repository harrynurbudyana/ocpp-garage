from typing import List

from pydantic import BaseModel

from views import PaginationView
from views.charge_points import ConnectorView


class CreateDriverView(BaseModel):
    email: str
    first_name: str
    last_name: str
    address: str


class UpdateDriverView(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    charge_point_id: str | None = None
    connector_id: int | None = None
    is_active: bool | None = None


class SimpleDriverView(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    address: str
    is_active: bool

    class Config:
        orm_mode = True


class DriverView(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    address: str
    is_active: bool
    connectors: List[ConnectorView]

    class Config:
        orm_mode = True


class PaginatedDriversView(BaseModel):
    items: List[SimpleDriverView]
    pagination: PaginationView
