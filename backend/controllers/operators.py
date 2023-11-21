import http
from typing import Tuple

from fastapi import Response, Request, Depends, BackgroundTasks
from loguru import logger
from starlette import status

from core.database import get_contextual_session
from core.fields import NotificationType
from exceptions import NotAuthenticated
from models import Operator
from routers import AnonymousRouter, AuthenticatedRouter
from services.auth import create_token, cookie_name, pwd_context, generate_random_password
from services.garages import list_simple_garages
from services.notifications import send_notification
from services.operators import get_operator, build_operators_query, \
    create_operator
from utils import params_extractor, paginate
from views.operators import LoginView, PaginatedOperatorsView, ReadOperatorGaragesView, CreateOperatorView

operators_public_router = AnonymousRouter()
operators_private_router = AuthenticatedRouter()


@operators_private_router.get(
    "/me",
    status_code=http.HTTPStatus.OK,
    response_model=ReadOperatorGaragesView
)
async def retrieve_operator(request: Request):
    operator = request.state.operator
    response = ReadOperatorGaragesView(operator=operator)
    async with get_contextual_session() as session:
        if operator.is_superuser:
            response.garages = await list_simple_garages(session)
        else:
            response.garages = [operator.garage]
    return response


@operators_private_router.post("/logout")
async def logout():
    logger.info(f"Start logout.")
    raise NotAuthenticated


@operators_public_router.post(
    "/login",
    status_code=http.HTTPStatus.ACCEPTED,
    response_model=ReadOperatorGaragesView
)
async def login(response: Response, data: LoginView):
    logger.info(f"Start login (user={data.email})")
    error_message = "Invalid login or password"
    async with get_contextual_session() as session:
        operator = await get_operator(session, data.email)
        if not operator:
            raise NotAuthenticated(detail=error_message)

        if not pwd_context.verify(data.password, operator.password):
            raise NotAuthenticated(detail=error_message)

    token = await create_token(operator.garage_id, operator.id)
    response.set_cookie(cookie_name, token)
    response = ReadOperatorGaragesView(operator=operator)
    async with get_contextual_session() as session:
        if operator.is_superuser:
            response.garages = await list_simple_garages(session)
        else:
            response.garages = [operator.garage]
    return response


@operators_private_router.get(
    "/{garage_id}/operators",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedOperatorsView
)
async def retrieve_garage_drivers(
        garage_id: str,
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedOperatorsView:
    async with get_contextual_session() as session:
        criterias = [
            Operator.garage_id == garage_id
        ]
        items, pagination = await paginate(
            session,
            lambda: build_operators_query(search, extra_criterias=criterias),
            *params
        )
        return PaginatedOperatorsView(items=[item[0] for item in items], pagination=pagination)


@operators_private_router.post(
    "/{garage_id}/operators",
    status_code=status.HTTP_204_NO_CONTENT
)
async def add_operator(
        garage_id: str,
        data: CreateOperatorView,
        background_tasks: BackgroundTasks
):
    logger.info(f"Start create driver (data={data})")

    password = await generate_random_password()
    data.password = password

    async with get_contextual_session() as session:
        await create_operator(session, garage_id, data)
        await session.commit()

    background_tasks.add_task(
        send_notification,
        data.email,
        NotificationType.new_operator_invited,
        dict(password=password)
    )
