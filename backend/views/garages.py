from typing import List

from pydantic import BaseModel

from views import PaginationView


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
    postnummer: str
    grid_provider: str

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
    postnummer: str
    grid_provider: str

    class Config:
        orm_mode = True


class CreateGarageView(BaseModel):
    name: str
    city: str
    street: str
    contact: str
    phone: str
    email: str
    postnummer: str
    grid_provider: str


class PaginatedGaragesView(BaseModel):
    items: List[SimpleGarageView]
    pagination: PaginationView
