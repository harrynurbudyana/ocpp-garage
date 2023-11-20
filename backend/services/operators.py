from typing import List

from sqlalchemy import select, or_, func, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable

from models import Operator
from views.operators import CreateOperatorView


async def build_operators_query(search: str, extra_criterias: List | None = None) -> selectable:
    query = select(Operator)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(Operator.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(Operator.email).contains(func.lower(search)),
            func.cast(Operator.address, String).ilike(f"{search}%"),
            func.lower(Operator.first_name).contains(func.lower(search)),
            func.lower(Operator.last_name).contains(func.lower(search)),
        ))
    return query


async def get_operator(session: AsyncSession, value) -> Operator:
    result = await session.execute(select(Operator).where(or_(Operator.email == value, Operator.id == value)))
    return result.scalars().first()


async def create_operator(session: AsyncSession, garage_id: str | None, data: CreateOperatorView) -> Operator:
    from services.auth import pwd_context

    if not data.password:
        raise ValueError(f"Received empty 'password' field for operator. Need to set a value (data={data})")
    data.password = pwd_context.hash(data.password)
    operator = Operator(**data.dict())
    operator.garage_id = garage_id
    session.add(operator)
    return operator
