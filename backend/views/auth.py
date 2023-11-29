from http import HTTPStatus
from typing import List

from pydantic import BaseModel

from core.fields import Role
from views.garages import ShortGarageView


class NotAuthenticatedResponse(BaseModel):
    detail = "User is not authenticated"
    code = HTTPStatus.UNAUTHORIZED


class AuthToken(BaseModel):
    garage_id: str | None = None
    user_id: str
    expired: str


class PersonView(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool
    is_active: bool
    role: Role | None = None

    class Config:
        orm_mode = True


class ReadPersonGaragesView(BaseModel):
    user: PersonView
    garages: List[ShortGarageView] = []

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class InviteUserView(BaseModel):
    role: Role
    email: str
    garage_id: str | None = None
    id: str | None = None
