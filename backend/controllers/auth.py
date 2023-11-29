import http

from loguru import logger
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import Response

from controllers.drivers import cache
from core.database import get_contextual_session
from exceptions import NotAuthenticated, NotFound
from routers import AnonymousRouter, AuthenticatedRouter
from services.auth import pwd_context, create_token, cookie_name, invite_user
from services.drivers import find_driver
from services.garages import list_simple_garages
from services.operators import get_operator
from views import LoginView
from views.auth import ReadPersonGaragesView, InviteUserView

auth_public_router = AnonymousRouter()
auth_router = AuthenticatedRouter(
    prefix="/{garage_id}"
)


@auth_public_router.post(
    "/login",
    status_code=http.HTTPStatus.ACCEPTED,
    response_model=ReadPersonGaragesView
)
async def login(response: Response, data: LoginView):
    logger.info(f"Start login (user={data.email})")
    error_message = "Invalid login or password"
    async with get_contextual_session() as session:
        operator = await get_operator(session, data.email)
        driver = await find_driver(session, data.email)
        user = operator or driver
        if not user:
            raise NotAuthenticated(detail=error_message)

        if not pwd_context.verify(data.password, user.password):
            raise NotAuthenticated(detail=error_message)

    token = await create_token(user.garage_id, user.id)
    response.set_cookie(cookie_name, token)
    response = ReadPersonGaragesView(user=user)
    async with get_contextual_session() as session:
        if user.is_superuser:
            response.garages = await list_simple_garages(session)
        else:
            response.garages = [user.garage]
    return response


@auth_public_router.post("/logout")
async def logout():
    logger.info(f"Start logout.")
    raise NotAuthenticated


@auth_router.post(
    "/invite",
    status_code=status.HTTP_204_NO_CONTENT
)
async def send_invitation_link(
        garage_id: str,
        data: InviteUserView,
        background_tasks: BackgroundTasks
):
    logger.info(f"Start invite driver (data={data})")
    await invite_user(garage_id, data, background_tasks)


@auth_public_router.get(
    "/drivers/signup/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=InviteUserView
)
async def check_invitation_link(user_id: str):
    data = await cache.get(user_id)
    if not data:
        raise NotFound
    return data
