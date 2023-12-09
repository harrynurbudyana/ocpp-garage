from typing import List

from sqlalchemy import select, update, func, or_, String, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable

from exceptions import NotFound
from models import ChargePoint, Connector, Garage
from pyocpp_contrib.v16.views.events import StatusNotificationCallEvent
from views.charge_points import CreateChargPointView, UpdateChargPointView


async def create_or_update_connector(
        session: AsyncSession,
        event: StatusNotificationCallEvent
) -> None:
    try:
        await get_connector_or_404(
            session,
            event.charge_point_id,
            event.payload.connector_id
        )
    except NotFound:
        connector = Connector(
            id=event.payload.connector_id,
            charge_point_id=event.charge_point_id,
            error_code=event.payload.error_code
        )
        session.add(connector)
    else:
        data = UpdateChargPointView(
            status=event.payload.status,
            error_code=event.payload.error_code
        )
        await update_connector(
            session,
            event.charge_point_id,
            event.payload.connector_id,
            data
        )


async def update_connectors(
        session: AsyncSession,
        charge_point_id: str,
        data: UpdateChargPointView
) -> None:
    await session.execute(
        update(Connector) \
            .where(Connector.charge_point_id == charge_point_id) \
            .values(**data.dict(exclude_unset=True))
    )


async def update_connector(
        session: AsyncSession,
        charge_point_id: str,
        connector_id: int,
        data: UpdateChargPointView
) -> None:
    await session.execute(
        update(Connector) \
            .where(Connector.charge_point_id == charge_point_id,
                   Connector.id == connector_id) \
            .values(**data.dict(exclude_unset=True))
    )


async def build_charge_points_query(
        search: str | None = None,
        extra_criterias: List | None = None
) -> selectable:
    criterias = [
        ChargePoint.is_active.is_(True)
    ]
    if extra_criterias:
        criterias.extend(extra_criterias)
    query = select(ChargePoint).outerjoin(Connector)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(ChargePoint.updated_at.asc())
    if search:
        query = query.where(
            or_(
                func.lower(ChargePoint.id).contains(func.lower(search)),
                func.cast(ChargePoint.status, String).ilike(f"{search}%"),
                func.lower(ChargePoint.location).contains(func.lower(search)),
            )
        )
    return query


async def get_charge_point_or_404(
        session: AsyncSession,
        charge_point_id
) -> ChargePoint:
    query = select(ChargePoint).outerjoin(Garage).where(ChargePoint.id == charge_point_id)
    result = await session.execute(query)
    charge_point = result.scalars().first()
    if not charge_point:
        raise NotFound(detail="The station is not found.")
    return charge_point


async def get_connector_or_404(
        session: AsyncSession,
        charge_point_id,
        connector_id
) -> Connector:
    query = select(Connector) \
        .outerjoin(ChargePoint) \
        .where(ChargePoint.id == charge_point_id, Connector.id == connector_id)
    result = await session.execute(query)
    connector = result.scalars().first()
    if not connector:
        raise NotFound(detail="The connector is not found.")
    return connector


async def create_charge_point(
        session: AsyncSession,
        garage_id: str,
        data: CreateChargPointView
) -> ChargePoint:
    charge_point = ChargePoint(garage_id=garage_id, **data.dict())
    session.add(charge_point)
    return charge_point


async def update_charge_point(
        session: AsyncSession,
        charge_point_id: str,
        data: UpdateChargPointView
) -> ChargePoint:
    await session.execute(update(ChargePoint).returning(ChargePoint) \
                          .where(ChargePoint.id == charge_point_id) \
                          .values(**data.dict(exclude_unset=True)))
    return await get_charge_point_or_404(session, charge_point_id)


async def remove_charge_point(
        session: AsyncSession,
        charge_point_id: str
) -> None:
    query = delete(ChargePoint).where(ChargePoint.id == charge_point_id)
    await session.execute(query)


async def list_simple_charge_points(
        session: AsyncSession,
        garage_id: str
) -> List[ChargePoint]:
    query = select(ChargePoint) \
        .join(Connector, Connector.charge_point_id == ChargePoint.id) \
        .where(ChargePoint.garage_id == garage_id)
    query = query.with_only_columns(
        ChargePoint.id,
        ChargePoint.location,
        ChargePoint.status
    )
    result = await session.execute(query)
    return result.unique().fetchall()
