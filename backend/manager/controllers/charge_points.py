from typing import Tuple, List

from fastapi import status, Depends
from loguru import logger

from core.database import get_contextual_session
from manager.models import ChargePoint
from manager.routers import AuthenticatedRouter
from manager.services.charge_points import (
    get_charge_point,
    create_charge_point,
    build_charge_points_query,
    remove_charge_point, update_charge_point, list_simple_charge_points
)
from manager.utils import params_extractor, paginate
from manager.views.charge_points import PaginatedChargePointsView, CreateChargPointView, ChargePointView, \
    UpdateChargPointView, SimpleChargePoint

charge_points_router = AuthenticatedRouter(
    prefix="/charge_points",
    tags=["charge_points"]
)


@charge_points_router.get(
    "/autocomplete",
    status_code=status.HTTP_200_OK,
    response_model=List[SimpleChargePoint]
)
async def retrieve_simple_charge_points() -> List[ChargePoint]:
    async with get_contextual_session() as session:
        return await list_simple_charge_points(session)


@charge_points_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_charge_points(
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedChargePointsView:
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_charge_points_query(search),
            *params
        )
        return PaginatedChargePointsView(items=[item[0] for item in items], pagination=pagination)


@charge_points_router.get(
    "/{charge_point_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChargePointView
)
async def retrieve_charge_point(
        charge_point_id: str
):
    async with get_contextual_session() as session:
        return await get_charge_point(session, charge_point_id)


@charge_points_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_charge_point(
        data: CreateChargPointView
):
    logger.info(f"Start create charge point (data={data})")
    async with get_contextual_session() as session:
        await create_charge_point(session, data)
        await session.commit()


@charge_points_router.put(
    "/{charge_point_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ChargePointView
)
async def edit_charge_point(
        charge_point_id: str,
        data: UpdateChargPointView
):
    logger.info(f"Start update charge point (data={data})")
    async with get_contextual_session() as session:
        await update_charge_point(session, charge_point_id, data)
        await session.commit()
        return await get_charge_point(session, charge_point_id)


@charge_points_router.delete(
    "/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_charge_point(
        charge_point_id: str
):
    logger.info(f"Start remove charge point (id={charge_point_id})")
    async with get_contextual_session() as session:
        await remove_charge_point(session, charge_point_id)
        await session.commit()
