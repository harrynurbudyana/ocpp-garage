import http
from typing import Tuple

from fastapi import Request, Depends
from loguru import logger
from pyocpp_contrib.cache import get_connection
from starlette import status

from core.database import get_contextual_session
from models import User
from routers import AuthenticatedRouter, AnonymousRouter
from services.garages import list_simple_garages
from services.users import (
    build_users_query,
    create_user
)
from utils import params_extractor, paginate
from views.users import ReadUsersGaragesView, PaginatedUsersView, CreateUserView

private_router = AuthenticatedRouter()
public_router = AnonymousRouter()


@private_router.get(
    "/me",
    status_code=http.HTTPStatus.OK,
    response_model=ReadUsersGaragesView
)
async def retrieve_user(request: Request):
    user = request.state.user
    response = ReadUsersGaragesView(user=user)
    async with get_contextual_session() as session:
        if user.is_superuser:
            response.garages = await list_simple_garages(session)
        else:
            response.garages = [user.garage]
    return response


@private_router.get(
    "/{garage_id}/users",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedUsersView
)
async def list_users(
        garage_id: str,
        request: Request,
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedUsersView:
    async with get_contextual_session() as session:
        criterias = [
            User.garage_id == garage_id,
            User.is_superuser.is_(False),
            User.id != request.state.user.id
        ]
        items, pagination = await paginate(
            session,
            lambda: build_users_query(search, extra_criterias=criterias),
            *params
        )
        return PaginatedUsersView(items=[item[0] for item in items], pagination=pagination)


@public_router.post(
    "/{garage_id}/users",
    status_code=status.HTTP_204_NO_CONTENT
)
async def add_user(
        garage_id: str,
        data: CreateUserView
):
    logger.info(f"Start create user (data={data})")

    async with get_contextual_session() as session:
        await create_user(session, data, garage_id)
        await session.commit()

    connection = await get_connection()
    await connection.delete(data.id)
