from typing import List

from pydantic import BaseModel

from views import PaginationView


class CreateOperatorView(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    address: str


class LoginView(BaseModel):
    email: str
    password: str


class ReadOperatorView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool

    class Config:
        orm_mode = True


class SimpleOperatorView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None

    class Config:
        orm_mode = True


class PaginatedOperatorsView(BaseModel):
    items: List[SimpleOperatorView]
    pagination: PaginationView
