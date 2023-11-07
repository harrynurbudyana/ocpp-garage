from __future__ import annotations

from typing import List

import arrow
from sqlalchemy import extract
from sqlalchemy import select, update, delete
from sqlalchemy.sql import selectable

from models import GovernmentRebate
from views.government_rebates import CreateGovernmentRebateView, UpdateGovernmentRebateView


async def get_rebate(session, garage_id: str, month: int, year: int) -> GovernmentRebate:
    query = await session.execute(
        select(GovernmentRebate) \
            .where(GovernmentRebate.garage_id == garage_id) \
            .where(extract("month", GovernmentRebate.period) == month,
                   extract("year", GovernmentRebate.period) == year)
    )
    rebate = query.scalars().first()
    return rebate


async def list_available_rebates(session, garage_id: str) -> List[GovernmentRebate]:
    query = select(GovernmentRebate) \
        .where(GovernmentRebate.garage_id == garage_id).with_only_columns(GovernmentRebate.period)
    result = await session.execute(query)
    return result.unique().fetchall()


async def build_government_rebates_query(extra_criterias: List | None = None) -> selectable:
    query = select(GovernmentRebate)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(GovernmentRebate.created_at.desc())
    return query


async def create_or_update_government_rebate(session, garage_id: str, data: CreateGovernmentRebateView):
    rebate = await get_rebate(session, garage_id, data.month, data.year)
    if rebate:
        rebate.value = data.value
    else:
        rebate = GovernmentRebate(
            garage_id=garage_id,
            value=data.value,
            period=arrow.get(year=data.year, month=data.month, day=1)
        )
    session.add(rebate)
    return rebate


async def update_government_rebate(
        session,
        garage_id: str,
        government_rebate_id: str,
        data: UpdateGovernmentRebateView
) -> None:
    payload = data.dict(exclude_unset=True)
    if payload:
        await session.execute(update(GovernmentRebate) \
                              .where(GovernmentRebate.id == government_rebate_id) \
                              .where(GovernmentRebate.garage_id == garage_id) \
                              .values(**payload))


async def remove_government_rebate(session, garage_id: str, government_rebate_id: str) -> None:
    query = delete(GovernmentRebate) \
        .where(GovernmentRebate.id == government_rebate_id) \
        .where(GovernmentRebate.garage_id == garage_id)
    await session.execute(query)
