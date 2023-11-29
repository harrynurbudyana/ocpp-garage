import http
from typing import Tuple

from fastapi import Request, Depends
from loguru import logger
from starlette import status

from core.cache import Cache
from core.database import get_contextual_session
from models import Operator
from routers import AuthenticatedRouter, AnonymousRouter
from services.garages import list_simple_garages
from services.operators import build_operators_query, \
    create_operator
from utils import params_extractor, paginate
from views.auth import ReadPersonGaragesView
from views.operators import PaginatedOperatorsView, CreateOperatorView

operators_private_router = AuthenticatedRouter()
anonymous_operators_router = AnonymousRouter()

cache = Cache()


@operators_private_router.get(
    "/me",
    status_code=http.HTTPStatus.OK,
    response_model=ReadPersonGaragesView
)
async def retrieve_operator(request: Request):
    user = request.state.user
    response = ReadPersonGaragesView(user=user)
    async with get_contextual_session() as session:
        if user.is_superuser:
            response.garages = await list_simple_garages(session)
        else:
            response.garages = [user.garage]
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


@anonymous_operators_router.post(
    "/{garage_id}/operators",
    status_code=status.HTTP_204_NO_CONTENT
)
async def add_operator(
        garage_id: str,
        data: CreateOperatorView
):
    logger.info(f"Start create driver (data={data})")

    async with get_contextual_session() as session:
        await create_operator(session, garage_id, data)
        await session.commit()

    await cache.conn.delete(data.id)
