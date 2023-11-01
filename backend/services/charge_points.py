from __future__ import annotations

from typing import List

from pyocpp_contrib.v16.views.events import StatusNotificationCallEvent
from sqlalchemy import select, update, func, or_, String, delete
from sqlalchemy.sql import selectable

import models as models
from models import ChargePoint
from views.charge_points import CreateChargPointView, ChargePointUpdateStatusView


async def create_or_update_connector(session, event: StatusNotificationCallEvent):
    connector = await get_connector(session, event.charge_point_id, event.payload.connector_id)
    if not connector:
        connector = models.Connector(
            id=event.payload.connector_id,
            charge_point_id=event.charge_point_id,
            error_code=event.payload.error_code
        )
        session.add(connector)
    else:
        data = ChargePointUpdateStatusView(
            status=event.payload.status,
            error_code=event.payload.error_code
        )
        await update_connector(session, event.charge_point_id, event.payload.connector_id, data)


async def update_connectors(session, charge_point_id: str, data: ChargePointUpdateStatusView):
    await session.execute(
        update(models.Connector) \
            .where(models.Connector.charge_point_id == charge_point_id) \
            .values(**data.dict(exclude_unset=True))
    )


async def update_connector(session, charge_point_id: str, connector_id: int, data: ChargePointUpdateStatusView):
    await session.execute(
        update(models.Connector) \
            .where(models.Connector.charge_point_id == charge_point_id,
                   models.Connector.id == connector_id) \
            .values(**data.dict(exclude_unset=True))
    )


async def build_charge_points_query(search: str, extra_criterias: List | None = None) -> selectable:
    criterias = [
        ChargePoint.is_active.is_(True)
    ]
    if extra_criterias:
        criterias.extend(extra_criterias)
    query = select(ChargePoint).outerjoin(models.Connector).outerjoin(models.Driver)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(ChargePoint.updated_at.asc())
    if search:
        query = query.where(
            or_(
                func.lower(ChargePoint.id).contains(func.lower(search)),
                func.cast(ChargePoint.status, String).ilike(f"{search}%"),
                func.lower(ChargePoint.location).contains(func.lower(search)),
                func.lower(models.Driver.email).contains(func.lower(search)),
                func.lower(models.Driver.last_name).contains(func.lower(search))
            )
        )
    return query


async def get_charge_point(session, charge_point_id) -> ChargePoint | None:
    query = select(ChargePoint).outerjoin(models.Garage).where(ChargePoint.id == charge_point_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_connector(session, charge_point_id, connector_id) -> ChargePoint | None:
    query = select(models.Connector) \
        .outerjoin(models.ChargePoint) \
        .where(models.ChargePoint.id == charge_point_id, models.Connector.id == connector_id)
    result = await session.execute(query)
    return result.scalars().first()


async def create_charge_point(session, garage_id: str, data: CreateChargPointView):
    charge_point = ChargePoint(garage_id=garage_id, **data.dict())
    session.add(charge_point)
    return charge_point


async def update_charge_point(
        session,
        charge_point_id: str,
        data
) -> None:
    await session.execute(update(ChargePoint) \
                          .where(ChargePoint.id == charge_point_id) \
                          .values(**data.dict(exclude_unset=True)))


async def remove_charge_point(session, charge_point_id: str) -> None:
    query = delete(ChargePoint).where(ChargePoint.id == charge_point_id)
    await session.execute(query)


async def list_simple_charge_points(session, garage_id: str, all=False) -> List[ChargePoint]:
    query = select(ChargePoint) \
        .join(models.Connector, models.Connector.charge_point_id == ChargePoint.id) \
        .where(ChargePoint.garage_id == garage_id)
    if not all:
        query = query.where(ChargePoint.connectors.any(models.Connector.driver_id.is_(None)))
    query = query.with_only_columns(
        ChargePoint.id,
        ChargePoint.location,
        ChargePoint.status
    )
    result = await session.execute(query)
    return result.unique().fetchall()


async def release_connector(session, driver_id: str, charge_point_id: str, connector_id: int):
    await session.execute(update(models.Connector) \
                          .where(models.Connector.driver_id == driver_id,
                                 models.Connector.charge_point_id == charge_point_id,
                                 models.Connector.id == connector_id) \
                          .values({"driver_id": None}))
