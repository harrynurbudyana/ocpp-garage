from __future__ import annotations

from typing import Callable

import arrow
from faker import Faker
from fastapi.routing import APIRoute
from jose import jwt
from passlib.context import CryptContext
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response

from core import settings
from core.cache import Cache
from core.database import get_contextual_session, generate_default_id
from core.fields import NotificationType
from core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, UTC_DATETIME_FORMAT
from core.utils import now
from services.drivers import get_driver
from services.operators import get_operator
from views.auth import AuthToken, InviteUserView


async def extract_token(request: Request) -> AuthToken | str:
    token = request.cookies.get(cookie_name)

    try:
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return AuthToken(**token)
    except Exception:
        return ""


async def create_token(garage_id: str, user_id: str) -> str:
    token = AuthToken(
        garage_id=garage_id,
        user_id=str(user_id),
        expired=now().shift(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) \
            .datetime.strftime(UTC_DATETIME_FORMAT)
    )

    return jwt.encode(token.dict(), SECRET_KEY, algorithm=ALGORITHM)


async def refresh_token(request: Request, response: Response):
    old_token = await extract_token(request)
    if not old_token:
        return
    new_token = await create_token(old_token.garage_id, old_token.user_id)
    response.set_cookie(cookie_name, new_token)


class AuthRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        from exceptions import NotAuthenticated

        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            token = await extract_token(request)
            if not token:
                raise NotAuthenticated

            async with get_contextual_session() as session:
                user = await get_operator(session, token.user_id) \
                       or await get_driver(session, token.garage_id, token.user_id)

                if arrow.get(token.expired) < now() or not user:
                    raise NotAuthenticated

                request.state.user = user

            response: Response = await original_route_handler(request)
            return response

        return custom_route_handler


cookie_name = "token"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def generate_random_password(length: int = 10) -> str:
    Faker.seed(0)
    faker = Faker()
    return faker.lexify(text='?' * length)


async def invite_user(garage_id: str, data: InviteUserView, background_tasks: BackgroundTasks):
    from services.notifications import send_notification

    data.garage_id = garage_id
    data.id = generate_default_id()
    cache = Cache()
    await cache.set(data.id, data.dict(), settings.INVITATION_LINK_EXPIRE_AFTER)

    link = settings.ALLOWED_ORIGIN + f"/signup/{data.id}"

    background_tasks.add_task(
        send_notification,
        data.email,
        NotificationType.new_user_invited,
        dict(link=link)
    )
