import http
import json

from fastapi import Request
from loguru import logger
from pyocpp_contrib.cache import get_connection
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import Response

from core.database import get_contextual_session
from core.fields import Role
from exceptions import NotAuthenticated, NotFound
from routers import AnonymousRouter, AuthenticatedRouter
from services.auth import create_token, cookie_name
from services.garages import list_simple_garages
from services.users import get_user_or_404, pwd_context, invite_user
from views import LoginView
from views.users import InviteUserView, ReadUsersGaragesView

public_router = AnonymousRouter()
private_router = AuthenticatedRouter(
    prefix="/{garage_id}"
)


@public_router.post(
    "/login",
    status_code=http.HTTPStatus.ACCEPTED,
    response_model=ReadUsersGaragesView
)
async def login(response: Response, data: LoginView):
    logger.info(f"Start login (user={data.email})")
    error_message = "Invalid login or password"
    async with get_contextual_session() as session:
        try:
            user = await get_user_or_404(session, data.email)
        except NotFound:
            raise NotAuthenticated(detail=error_message)

        if not pwd_context.verify(data.password, user.password):
            raise NotAuthenticated(detail=error_message)

        token = await create_token(user.id)
        response.set_cookie(cookie_name, token)
        response = ReadUsersGaragesView(user=user)
        if user.is_superuser:
            response.garages = await list_simple_garages(session)
        else:
            response.garages = [user.garage]
        return response


@public_router.post("/logout")
async def logout():
    raise NotAuthenticated


@private_router.post(
    "/invite",
    status_code=status.HTTP_204_NO_CONTENT
)
async def send_invitation_link(
        garage_id: str,
        data: InviteUserView,
        background_tasks: BackgroundTasks,
        request: Request
):
    logger.info(f"Start invite user (data={data})")
    if request.state.user.is_superuser:
        data.role = Role.admin
    else:
        data.role = Role.operator
    await invite_user(garage_id, data, background_tasks)


@public_router.get(
    "/users/signup/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=InviteUserView
)
async def check_invitation_link(user_id: str):
    connection = await get_connection()
    context: bytes | None = await connection.get(user_id)
    try:
        data = json.loads(context.decode())
    except AttributeError:
        data = None
    if not data:
        raise NotFound
    return data
