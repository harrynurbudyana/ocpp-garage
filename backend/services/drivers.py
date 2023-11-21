from __future__ import annotations

from typing import List, Tuple

from async_stripe import stripe
from loguru import logger
from sqlalchemy import select, update, func, or_, String, delete
from sqlalchemy.sql import selectable

from core import settings
from models import Driver, Garage, Connector
from services.charge_points import update_connector
from services.transactions import find_prevmonth_drivers_transaction
from views.charge_points import UpdateChargPointView
from views.drivers import CreateDriverView, UpdateDriverView

stripe.api_key = settings.STRIPE_API_KEY


async def is_driver_authorized(driver: Driver):
    return driver.is_active


async def is_driver_debtor(session, driver: Driver) -> Tuple[bool, int, int]:
    logger.info(f"Check if driver is debtor (driver={driver})")
    transaction = await find_prevmonth_drivers_transaction(session, driver)

    if not transaction:
        return False, 0, 0

    items = await stripe.PaymentIntent.list(customer=driver.customer_id, limit=1)
    if not items.data:
        return True, int(transaction.month), int(transaction.year)

    item = items.data[0]

    intent = stripe.PaymentIntent.construct_from(item, settings.STRIPE_API_KEY)
    is_debtor = all([int(intent.metadata["month"]) == int(transaction.month),
                     int(intent.metadata["year"]) == int(transaction.year)])
    return is_debtor, int(transaction.month), int(transaction.year)


async def build_drivers_query(search: str, extra_criterias: List | None = None) -> selectable:
    query = select(Driver)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(Driver.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(Garage.name).contains(func.lower(search)),
            func.lower(Driver.email).contains(func.lower(search)),
            func.cast(Driver.address, String).ilike(f"{search}%"),
            func.lower(Driver.first_name).contains(func.lower(search)),
            func.lower(Driver.last_name).contains(func.lower(search)),
        ))
    return query


async def get_driver(session, garage_id, driver_id) -> Driver | None:
    result = await session.execute(
        select(Driver) \
            .where(Driver.id == driver_id) \
            .where(Driver.garage_id == garage_id)
    )
    return result.scalars().first()


async def find_driver(session, customer_id: str) -> Driver | None:
    result = await session.execute(
        select(Driver) \
            .where(Driver.customer_id == customer_id)
    )
    return result.scalars().first()


async def create_driver(session, garage_id: str, data: CreateDriverView):
    customer = await stripe.Customer.create()
    driver = Driver(garage_id=garage_id, customer_id=customer.id, **data.dict())
    session.add(driver)
    return driver


async def update_driver(
        session,
        garage_id: str,
        driver_id: str,
        data: UpdateDriverView
) -> None:
    payload = data.dict(exclude_unset=True)
    charge_point_id = payload.pop("charge_point_id", None)
    connector_id = payload.pop("connector_id", None)
    if charge_point_id and connector_id:
        data = UpdateChargPointView(driver_id=driver_id)
        await update_connector(session, charge_point_id, connector_id, data)
    if payload:
        await session.execute(update(Driver) \
                              .where(Driver.id == driver_id) \
                              .where(Driver.garage_id == garage_id) \
                              .values(**payload))


async def remove_driver(session, garage_id: str, driver_id: str) -> None:
    await session.execute(update(Connector) \
                          .where(Connector.driver_id == driver_id) \
                          .values({"driver_id": None}))
    driver = await get_driver(session, garage_id, driver_id)
    query = delete(Driver) \
        .where(Driver.id == driver_id) \
        .where(Driver.garage_id == garage_id)
    await stripe.Customer.delete(driver.customer_id)
    await session.execute(query)
