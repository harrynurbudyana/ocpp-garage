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
    address: str
    contact: str
    phone: str

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
    address: str
    contact: str
    phone: str
    grid_provider: str

    class Config:
        orm_mode = True


class CreateGarageView(BaseModel):
    name: str
    address: str
    contact: str
    phone: str
    grid_provider: str

    class Config:
        orm_mode = True


class PaginatedGaragesView(BaseModel):
    items: List[SimpleGarageView]
    pagination: PaginationView
