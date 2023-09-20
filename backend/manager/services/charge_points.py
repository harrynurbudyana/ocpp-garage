from __future__ import annotations

from sqlalchemy import select, update, func, or_, String, delete
from sqlalchemy.sql import selectable

import manager.models as models
from manager.models import ChargePoint
from manager.views.charge_points import CreateChargPointView, UpdateChargPointView


async def build_charge_points_query(search: str) -> selectable:
    criterias = [
        ChargePoint.is_active.is_(True)
    ]
    query = select(ChargePoint).outerjoin(models.Driver)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(ChargePoint.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(ChargePoint.id).contains(func.lower(search)),
            func.cast(ChargePoint.status, String).ilike(f"{search}%"),
            func.lower(ChargePoint.location).contains(func.lower(search)),
            func.lower(models.Driver.first_name).contains(func.lower(search)),
            func.lower(models.Driver.last_name).contains(func.lower(search))
        ))
    return query


async def get_charge_point(session, charge_point_id) -> ChargePoint | None:
    result = await session.execute(select(ChargePoint).where(ChargePoint.id == charge_point_id))
    return result.scalars().first()


async def create_charge_point(session, data: CreateChargPointView):
    charge_point = ChargePoint(**data.dict())
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
        query = delete(ChargePoint) \
            .where(ChargePoint.id == charge_point_id)
        await session.execute(query)
