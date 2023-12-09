from typing import List

from pydantic import BaseModel

from core.fields import Role
from views import PaginationView
from views.garages import ShortGarageView


class CreateUserView(BaseModel):
    address: str | None = None
    email: str
    first_name: str
    id: str | None = None
    last_name: str | None = None
    password: str
    role: Role | None = None
    is_superuser: bool = False


class SimpleUserView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    is_active: bool
    role: Role

    class Config:
        orm_mode = True


class PaginatedUsersView(BaseModel):
    items: List[SimpleUserView]
    pagination: PaginationView


class InviteUserView(BaseModel):
    role: Role | None = None
    email: str
    garage_id: str | None = None
    id: str | None = None


class UserView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool
    is_admin: bool
    is_operator: bool
    is_active: bool

    class Config:
        orm_mode = True


class ReadUsersGaragesView(BaseModel):
    user: UserView
    garages: List[ShortGarageView] = []

    class Config:
        orm_mode = True
