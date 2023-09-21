from typing import List

from pydantic import BaseModel

from manager.views import PaginationView
from manager.views.charge_points import SimpleChargePoint


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


class SimpleDriverView(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    address: str

    class Config:
        orm_mode = True


class DriverView(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    address: str
    charge_points: List[SimpleChargePoint]

    class Config:
        orm_mode = True


class PaginatedDriversView(BaseModel):
    items: List[SimpleDriverView]
    pagination: PaginationView
