from __future__ import annotations

from typing import List

from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable

from exceptions import NotFound
from models import Garage, GridProvider
from views.garages import CreateGarageView, GarageRatesView


async def list_simple_garages(session: AsyncSession) -> List[Garage]:
    query = select(Garage).with_only_columns(Garage.id, Garage.name)
    result = await session.execute(query)
    return result.unique().fetchall()


async def build_garages_query(
        search: str,
        extra_criterias: List | None = None
) -> selectable:
    criterias = [
        Garage.is_active.is_(True)
    ]
    if extra_criterias:
        criterias.extend(extra_criterias)
    query = select(Garage)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(Garage.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(Garage.name).contains(func.lower(search)),
            func.lower(Garage.city).contains(func.lower(search)),
            func.lower(Garage.contact).contains(func.lower(search)),
            func.lower(Garage.postnummer).contains(func.lower(search)),
        ))
    return query


async def get_garage_or_404(session: AsyncSession, garage_id: str) -> selectable:
    result = await session.execute(select(Garage).where(Garage.id == garage_id))
    garage = result.scalars().first()
    if not garage:
        raise NotFound(detail="Tha garage is not found.")
    return garage


async def create_garage(
        session: AsyncSession,
        data: CreateGarageView
) -> Garage:
    query = await session.execute(select(GridProvider).where(GridProvider.id == data.grid_provider_id))
    provider = query.scalars().first()
    garage = Garage(**data.dict())
    garage.daily_rate = provider.daily_rate
    garage.nightly_rate = provider.nightly_rate
    session.add(garage)
    await session.flush()
    return garage


async def delete_garage(session: AsyncSession, garage_id: str) -> None:
    await session.execute(delete(Garage).where(Garage.id == garage_id))


async def store_rates(
        session: AsyncSession,
        garage_id: str,
        data: GarageRatesView
) -> None:
    query = update(Garage) \
        .where(Garage.id == garage_id) \
        .values(daily_rate=round(data.daily.garage_rate, 2),
                nightly_rate=round(data.nightly.garage_rate, 2))
    await session.execute(query)
