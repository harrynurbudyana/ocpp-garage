import os
from typing import Tuple

import pdfkit
from fastapi import status, Depends, BackgroundTasks, Request
from fastapi.responses import FileResponse
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from controllers.payments import payments_router
from core.cache import Cache
from core.database import get_contextual_session
from core.settings import STATIC_PATH
from exceptions import NotFound
from models import Driver
from routers import AuthenticatedRouter, AnonymousRouter
from services.charge_points import release_connector
from services.drivers import (
    build_drivers_query,
    get_driver,
    create_driver,
    update_driver,
    remove_driver
)
from services.garages import get_garage
from services.payments import generate_payment_link
from services.statements import generate_statement_for_driver
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

anonymous_driver_router = AnonymousRouter()

cache = Cache()


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
async def retrieve_driver(
        garage_id: str,
        driver_id: str
):
    async with get_contextual_session() as session:
        return await get_driver(session, garage_id, driver_id)


@anonymous_driver_router.post(
    "/{garage_id}/drivers",
    status_code=status.HTTP_201_CREATED,
)
async def add_driver(
        garage_id: str,
        data: CreateDriverView
):
    result = await cache.get(data.id)
    if not result:
        raise NotFound

    logger.info(f"Start create driver (data={data})")
    async with get_contextual_session() as session:
        await create_driver(session, garage_id, data)
        await session.commit()

    await cache.conn.delete(data.id)


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
    "/{driver_id}/charge_points/{charge_point_id}/connectors/{connector_id}",
    status_code=status.HTTP_200_OK,
    response_model=DriverView
)
async def remove_charge_point(
        garage_id: str,
        driver_id: str,
        charge_point_id: str,
        connector_id: int
):
    logger.info(f"Releasing drivers charge point (driver_id={driver_id}, charge_point_id={charge_point_id})")
    async with get_contextual_session() as session:
        await release_connector(session, driver_id, charge_point_id, connector_id)
        await session.commit()
        return await get_driver(session, garage_id, driver_id)


@drivers_router.get(
    "/{driver_id}/statement",
    status_code=status.HTTP_200_OK
)
async def generate_statement(
        request: Request,
        background_task: BackgroundTasks,
        garage_id: str,
        driver_id: str,
        month: int,
        year: int
):
    async with get_contextual_session() as session:
        garage = await get_garage(session, garage_id)
        driver = await get_driver(session, garage_id, driver_id)
        transactions = await find_drivers_transactions(session, driver, month, year)
        statement = await generate_statement_for_driver(session, garage, driver, transactions, month, year)
    env = Environment(loader=FileSystemLoader('templates/statements'))
    template = env.get_template('driver.html')
    statement.payment_link = await generate_payment_link(
        request,
        payments_router,
        driver,
        statement.total_cost,
        month,
        year
    )
    html = template.render(**statement.dict())
    filename = driver.email.split("@")[0]
    filepath = os.path.join(STATIC_PATH, f"{filename}.pdf")
    pdfkit.from_string(html, filepath, verbose=True)
    background_task.add_task(os.remove, filepath)
    return FileResponse(filepath, media_type='application/pdf', filename=filepath.split("/")[-1])
