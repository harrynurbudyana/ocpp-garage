from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from typing import List

from ocpp.v16.call import StatusNotificationPayload
from pyocpp_contrib.v16.views.events import StatusNotificationCallEvent
from sqlalchemy import select, update, func, or_, String, delete
from sqlalchemy.sql import selectable

import models as models
from models import ChargePoint
from views.charge_points import CreateChargPointView


async def update_connectors(session, event: StatusNotificationCallEvent):
    charge_point = await get_charge_point(session, event.charge_point_id)
    connectors = deepcopy(charge_point.connectors)
    if not event.payload.connector_id:
        charge_point.status = event.payload.status
    else:
        for idx, data in enumerate(connectors):
            connector = StatusNotificationPayload(**data)
            if connector.connector_id == event.payload.connector_id:
                connectors[idx].update(asdict(event.payload))
                break
        else:
            connectors.append(asdict(event.payload))

    charge_point.connectors = connectors
    session.add(charge_point)


async def reset_connectors(session, charge_point_id: str):
    charge_point = await get_charge_point(session, charge_point_id)
    charge_point.connectors.clear()


async def build_charge_points_query(search: str, extra_criterias: List | None = None) -> selectable:
    criterias = [
        ChargePoint.is_active.is_(True)
    ]
    if extra_criterias:
        criterias.extend(extra_criterias)
    query = select(ChargePoint).outerjoin(models.Driver)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(ChargePoint.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(models.Garage.name).contains(func.lower(search)),
            func.lower(ChargePoint.id).contains(func.lower(search)),
            func.cast(ChargePoint.status, String).ilike(f"{search}%"),
            func.lower(ChargePoint.location).contains(func.lower(search)),
            func.lower(models.Driver.first_name).contains(func.lower(search)),
            func.lower(models.Driver.last_name).contains(func.lower(search))
        ))
    return query


async def get_charge_point(session, charge_point_id) -> ChargePoint | None:
    query = select(ChargePoint).where(ChargePoint.id == charge_point_id)
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
    query = select(ChargePoint).where(ChargePoint.garage_id == garage_id)
    if not all:
        query = query.where(ChargePoint.driver_id.is_(None))
    query = query.with_only_columns(ChargePoint.id, ChargePoint.location, ChargePoint.status, ChargePoint.connectors)
    result = await session.execute(query)
    return result.fetchall()


async def release_charge_point(session, driver_id: str, charge_point_id: str):
    await session.execute(update(ChargePoint) \
                          .where(ChargePoint.driver_id == driver_id,
                                 ChargePoint.id == charge_point_id) \
                          .values({"driver_id": None}))
