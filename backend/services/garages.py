from __future__ import annotations

from typing import List

from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.sql import selectable

import models as models
from views.garages import CreateGarageView, GarageRatesView


async def list_simple_garages(session):
    query = select(models.Garage).with_only_columns(models.Garage.id, models.Garage.name)
    result = await session.execute(query)
    return result.unique().fetchall()


async def build_garages_query(search: str, extra_criterias: List | None = None) -> selectable:
    criterias = [
        models.Garage.is_active.is_(True)
    ]
    if extra_criterias:
        criterias.extend(extra_criterias)
    query = select(models.Garage)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(models.Garage.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(models.Garage.name).contains(func.lower(search)),
            func.lower(models.Garage.city).contains(func.lower(search)),
            func.lower(models.Garage.contact).contains(func.lower(search)),
            func.lower(models.Garage.postnummer).contains(func.lower(search)),
        ))
    return query


async def get_garage(session, garage_id) -> selectable:
    result = await session.execute(select(models.Garage).where(models.Garage.id == garage_id))
    return result.scalars().first()


async def create_garage(session, data: CreateGarageView):
    query = await session.execute(select(models.GridProvider).where(models.GridProvider.id == data.grid_provider_id))
    provider = query.scalars().first()
    garage = models.Garage(**data.dict())
    garage.daily_rate = provider.daily_rate
    garage.nightly_rate = provider.nightly_rate
    session.add(garage)
    await session.flush()
    return garage


async def delete_garage(session, garage_id: str):
    await session.execute(delete(models.Garage).where(models.Garage.id == garage_id))


async def store_rates(session, garage_id: str, data: GarageRatesView):
    query = update(models.Garage) \
        .where(models.Garage.id == garage_id) \
        .values(daily_rate=round(data.daily.garage_rate, 2), nightly_rate=round(data.nightly.garage_rate, 2))
    await session.execute(query)
