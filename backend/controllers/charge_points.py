from typing import Tuple, List

from fastapi import status, Depends, HTTPException
from loguru import logger
from pyocpp_contrib.decorators import message_id_generator

from core.database import get_contextual_session
from exceptions import NotFound
from models import ChargePoint
from routers import AuthenticatedRouter, AnonymousRouter
from services.charge_points import (
    get_charge_point,
    create_charge_point,
    build_charge_points_query,
    remove_charge_point, update_charge_point, list_simple_charge_points
)
from services.ocpp.reset import process_reset
from services.ocpp.unlock_connector import process_unlock_connector
from utils import params_extractor, paginate
from views.charge_points import PaginatedChargePointsView, CreateChargPointView, ChargePointView, \
    UpdateChargPointView, SimpleChargePoint

charge_points_router = AuthenticatedRouter(
    prefix="/{garage_id}/charge_points",
    tags=["charge_points"]
)

anonymous_charge_points_router = AnonymousRouter()


@anonymous_charge_points_router.post(
    "/charge_points/{charge_point_id}",
    status_code=status.HTTP_200_OK
)
async def authenticate(charge_point_id: str):
    logger.info(f"Start authenticate charge point (charge_point_id={charge_point_id})")
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id=charge_point_id)
        if not charge_point:
            logger.error(f"Could not authenticate charge_point (charge_point_id={charge_point_id})")
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@charge_points_router.get(
    "/autocomplete",
    status_code=status.HTTP_200_OK,
    response_model=List[SimpleChargePoint]
)
async def retrieve_simple_charge_points(garage_id: str) -> List[ChargePoint]:
    async with get_contextual_session() as session:
        return await list_simple_charge_points(session, garage_id)


@charge_points_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_charge_points(
        garage_id: str,
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedChargePointsView:
    async with get_contextual_session() as session:
        criterias = [
            ChargePoint.garage_id == garage_id
        ]
        items, pagination = await paginate(
            session,
            lambda: build_charge_points_query(search, extra_criterias=criterias),
            *params
        )
        return PaginatedChargePointsView(items=[item[0] for item in items], pagination=pagination)


@charge_points_router.get(
    "/{charge_point_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChargePointView
)
async def retrieve_charge_point(
        garage_id: str,
        charge_point_id: str
):
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        if not charge_point:
            raise NotFound
        return charge_point


@charge_points_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_charge_point(
        garage_id: str,
        data: CreateChargPointView
):
    logger.info(f"Start create charge point (data={data})")
    async with get_contextual_session() as session:
        await create_charge_point(session, garage_id, data)
        await session.commit()


@charge_points_router.put(
    "/{charge_point_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ChargePointView
)
async def edit_charge_point(
        garage_id: str,
        charge_point_id: str,
        data: UpdateChargPointView
):
    logger.info(f"Start update charge point (data={data}, charge_point_id={charge_point_id})")
    async with get_contextual_session() as session:
        await update_charge_point(session, charge_point_id, data)
        await session.commit()
        return await get_charge_point(session, charge_point_id)


@charge_points_router.delete(
    "/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_charge_point(
        garage_id: str,
        charge_point_id: str
):
    logger.info(f"Start remove charge point (charge_point_id={charge_point_id})")
    async with get_contextual_session() as session:
        await remove_charge_point(session, charge_point_id)
        await session.commit()


@charge_points_router.put(
    "/{charge_point_id}/connectors/{connector_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def unlock_connector(
        garage_id: str,
        charge_point_id: str,
        connector_id: int
):
    logger.info(
        f"UnlockConnector -> | start process call request (charge_point_id={charge_point_id}, connector_id={connector_id})")
    async with get_contextual_session() as session:
        await process_unlock_connector(
            session,
            charge_point_id=charge_point_id,
            connector_id=connector_id,
            message_id=message_id_generator()
        )


@charge_points_router.patch(
    "/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def reset(garage_id: str, charge_point_id: str):
    logger.info(f"Reset -> | start process call request (charge_point_id={charge_point_id})")
    async with get_contextual_session() as session:
        await process_reset(
            session,
            charge_point_id=charge_point_id,
            message_id=message_id_generator()
        )
