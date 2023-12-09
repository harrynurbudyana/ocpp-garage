from __future__ import annotations

from typing import Callable

import arrow
from fastapi.routing import APIRoute
from jose import jwt
from starlette.requests import Request
from starlette.responses import Response

from exceptions import NotAuthenticated
from services.users import get_user_or_404
from core.database import get_contextual_session
from core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, UTC_DATETIME_FORMAT
from core.utils import now
from views.auth import AuthToken


cookie_name = "token"


async def extract_token(request: Request) -> AuthToken | str:
    token = request.cookies.get(cookie_name)
    try:
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return AuthToken(**token)
    except Exception:
        return ""


async def create_token(user_id: str) -> str:
    token = AuthToken(
        user_id=str(user_id),
        expired=now().shift(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) \
            .datetime.strftime(UTC_DATETIME_FORMAT)
    )

    return jwt.encode(token.dict(), SECRET_KEY, algorithm=ALGORITHM)


async def refresh_token(request: Request, response: Response):
    old_token = await extract_token(request)
    if not old_token:
        return
    new_token = await create_token(old_token.user_id)
    response.set_cookie(cookie_name, new_token)


class AuthRoute(APIRoute):
    def get_route_handler(self) -> Callable:

        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            token = await extract_token(request)
            if not token:
                raise NotAuthenticated

            async with get_contextual_session() as session:
                user = await get_user_or_404(session, token.user_id)

                if arrow.get(token.expired) < now() or not user:
                    raise NotAuthenticated

                request.state.user = user

            response: Response = await original_route_handler(request)
            return response

        return custom_route_handler


