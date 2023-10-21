from __future__ import annotations

from typing import List

import arrow
from sqlalchemy import extract
from sqlalchemy import select, update, delete
from sqlalchemy.sql import selectable

from models import GovernmentRebate
from views.government_rebates import CreateGovernmentRebateView, UpdateGovernmentRebateView


async def build_government_rebates_query(extra_criterias: List | None = None) -> selectable:
    query = select(GovernmentRebate)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(GovernmentRebate.created_at.desc())
    return query


async def create_government_rebate(session, garage_id: str, data: CreateGovernmentRebateView):
    query = await session.execute(
        select(GovernmentRebate) \
            .where(extract("month", GovernmentRebate.created_at) == arrow.utcnow().month)
    )
    rebate = query.scalars().first()
    if rebate:
        rebate.value = data.value
    else:
        rebate = GovernmentRebate(garage_id=garage_id, **data.dict())
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
