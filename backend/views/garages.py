from typing import List

from pydantic import BaseModel

from views import PaginationView
from views.grid_providers import GridProviderView


class NotPaginatedSimpleGarageView(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class SimpleGarageView(BaseModel):
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


class SingleGarageView(BaseModel):
    id: str
    name: str
    city: str
    street: str
    contact: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class SingleGarageWithProviderView(BaseModel):
    id: str
    name: str
    city: str
    street: str
    contact: str
    phone: str
    email: str
    grid_provider: GridProviderView

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


class PaginatedGaragesView(BaseModel):
    items: List[SimpleGarageView]
    pagination: PaginationView
