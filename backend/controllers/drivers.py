import os
from typing import Tuple

import arrow
import pdfkit
from fastapi import status, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from loguru import logger

from core.database import get_contextual_session
from core.settings import STATIC_PATH
from models import Driver
from routers import AuthenticatedRouter
from services.charge_points import release_charge_point
from services.drivers import (
    build_drivers_query,
    get_driver,
    create_driver,
    update_driver,
    remove_driver
)
from services.garages import get_garage
from services.statements import generate_statements_for_driver
from services.transactions import find_drivers_transactions
from utils import params_extractor, paginate
from views.drivers import (
    PaginatedDriversView,
    DriverView,
    CreateDriverView,
    UpdateDriverView
)

drivers_router = AuthenticatedRouter(
    prefix="/{garage_id}/drivers",
    tags=["drivers"]
)


@drivers_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def retrieve_drivers(
        garage_id: str,
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedDriversView:
    async with get_contextual_session() as session:
        criterias = [
            Driver.garage_id == garage_id
        ]
        items, pagination = await paginate(
            session,
            lambda: build_drivers_query(search, extra_criterias=criterias),
            *params
        )
        return PaginatedDriversView(items=[item[0] for item in items], pagination=pagination)


@drivers_router.get(
    "/{driver_id}",
    status_code=status.HTTP_200_OK,
    response_model=DriverView
)
async def retrieve_charge_point(
        garage_id: str,
        driver_id: str
):
    async with get_contextual_session() as session:
        return await get_driver(session, garage_id, driver_id)


@drivers_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_driver(
        garage_id: str,
        data: CreateDriverView
):
    logger.info(f"Start create driver (data={data})")
    async with get_contextual_session() as session:
        await create_driver(session, garage_id, data)
        await session.commit()


@drivers_router.put(
    "/{driver_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DriverView
)
async def edit_driver(
        garage_id: str,
        driver_id: str,
        data: UpdateDriverView
):
    logger.info(f"Start update driver (data={data})")
    async with get_contextual_session() as session:
        await update_driver(session, garage_id, driver_id, data)
        await session.commit()
        return await get_driver(session, garage_id, driver_id)


@drivers_router.delete(
    "/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_driver(
        garage_id: str,
        driver_id: str
):
    logger.info(f"Start remove driver (driver_id={driver_id})")
    async with get_contextual_session() as session:
        await remove_driver(session, garage_id, driver_id)
        await session.commit()


@drivers_router.delete(
    "/{driver_id}/charge_points/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_charge_point(
        garage_id: str,
        driver_id: str,
        charge_point_id: str
):
    logger.info(f"Releasing drivers charge point (driver_id={driver_id}, charge_point_id={charge_point_id})")
    async with get_contextual_session() as session:
        await release_charge_point(session, driver_id, charge_point_id)
        await session.commit()


@drivers_router.get(
    "/{driver_id}/statement",
    status_code=status.HTTP_200_OK
)
async def generate_statement(
        background_task: BackgroundTasks,
        garage_id: str,
        driver_id: str,
        month: int | None = None,
        year: int | None = None
):
    if not month:
        month = arrow.utcnow().month - 1  # previous one
    if not year:
        year = arrow.utcnow().year  # current one
    async with get_contextual_session() as session:
        garage = await get_garage(session, garage_id)
        driver = await get_driver(session, garage_id, driver_id)
        transactions = await find_drivers_transactions(session, driver, month, year)
    html = await generate_statements_for_driver(garage, driver, transactions, month, year)
    filename = driver.email.split("@")[0]
    filepath = os.path.join(STATIC_PATH, f"{filename}.pdf")
    pdfkit.from_string(html, filepath, verbose=True)
    background_task.add_task(os.remove, filepath)
    return FileResponse(filepath, media_type='application/pdf', filename=filepath.split("/")[-1])
