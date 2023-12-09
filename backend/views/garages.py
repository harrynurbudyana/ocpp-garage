from typing import List

from pydantic import BaseModel

from views import PaginationView


class GarageView(BaseModel):
    id: str
    name: str
    city: str
    street: str
    contact: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class ShortGarageView(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class CreateGarageView(BaseModel):
    name: str
    city: str
    street: str
    contact: str
    phone: str
    email: str
    grid_provider_id: str


class Rates(BaseModel):
    garage_rate: float
    provider_rate: float


class GarageRatesView(BaseModel):
    daily: Rates
    nightly: Rates


class StoreSettingsView(BaseModel):
    rates: GarageRatesView


class PaginatedGaragesView(BaseModel):
    items: List[GarageView]
    pagination: PaginationView
