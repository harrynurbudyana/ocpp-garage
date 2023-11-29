from typing import List

from pydantic import BaseModel

from core.fields import Role
from views import PaginationView


class CreateOperatorView(BaseModel):
    address: str
    email: str
    first_name: str
    id: str | None = None
    last_name: str
    password: str
    role: Role = Role.employee


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
