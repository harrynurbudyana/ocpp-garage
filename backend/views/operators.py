from typing import List

from pydantic import BaseModel

from views import PaginationView
from views.garages import ShortGarageView


class CreateOperatorView(BaseModel):
    email: str
    password: str | None = None
    first_name: str
    last_name: str
    address: str


class LoginView(BaseModel):
    email: str
    password: str


class OperatorView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool
    is_active: bool

    class Config:
        orm_mode = True


class ReadOperatorGaragesView(BaseModel):
    operator: OperatorView
    garages: List[ShortGarageView] = []

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class SimpleOperatorView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    is_active: bool

    class Config:
        orm_mode = True


class PaginatedOperatorsView(BaseModel):
    items: List[SimpleOperatorView]
    pagination: PaginationView
