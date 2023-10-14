from typing import Tuple

from fastapi import status, Depends
from loguru import logger

from core.database import get_contextual_session
from permissions.garages import CanOperatorManageGarages
from routers import AuthenticatedRouter
from services.garages import build_garages_query, create_garage
from utils import params_extractor, paginate
from views.garages import PaginatedGaragesView, SingleGarageView, CreateGarageView

garages_router = AuthenticatedRouter(
    prefix="/garages",
    tags=["garages"],
    dependencies=[Depends(CanOperatorManageGarages())]
)


@garages_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_garages(
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedGaragesView:
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_garages_query(search),
            *params
        )
        return PaginatedGaragesView(items=[item[0] for item in items], pagination=pagination)


@garages_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SingleGarageView
)
async def add_garage(
        data: CreateGarageView
):
    logger.info(f"Start create garage (data={data})")
    async with get_contextual_session() as session:
        garage = await create_garage(session, data)
        await session.commit()
        return garage
