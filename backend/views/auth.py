from http import HTTPStatus

from pydantic import BaseModel


class NotAuthenticatedResponse(BaseModel):
    detail = "User is not authenticated"
    code = HTTPStatus.UNAUTHORIZED


class AuthToken(BaseModel):
    garage_id: str | None = None
    user_id: str
    expired: str
