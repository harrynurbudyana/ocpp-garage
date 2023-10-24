from __future__ import annotations

from typing import List

from sqlalchemy import update, select, or_, func, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable

import models
from core.fields import TransactionStatus
from views.transactions import CreateTransactionView, UpdateTransactionView


async def create_transaction(
        session: AsyncSession,
        data: CreateTransactionView
) -> models.Transaction:
    transaction = models.Transaction(**data.dict())
    session.add(transaction)
    return transaction


async def update_transaction(
        session: AsyncSession,
        transaction_id: int,
        data: UpdateTransactionView
) -> None:
    await session.execute(
        update(models.Transaction) \
            .where(models.Transaction.transaction_id == transaction_id) \
            .values(**data.dict())
    )


async def get_transaction(session, transaction_id: str | int) -> models.Transaction | None:
    attr = models.Transaction.transaction_id if isinstance(transaction_id, int) else models.Transaction.id
    query = await session.execute(select(models.Transaction).where(attr == transaction_id))
    return query.scalars().first()


async def build_transactions_query(search: str, extra_criterias: List | None = None) -> selectable:
    query = select(models.Transaction)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(models.Transaction.transaction_id.desc())
    if search:
        query = query.where(or_(
            func.lower(models.Transaction.garage).contains(func.lower(search)),
            func.lower(models.Transaction.driver).contains(func.lower(search)),
            func.cast(models.Transaction.charge_point, String).ilike(f"{search}%"),
        ))
    return query


async def find_drivers_transactions(session, driver: models.Driver, month: int, year: int) -> List[models.Transaction]:
    query = select(models.Transaction) \
        .where(models.Transaction.driver == driver.email,
               models.Transaction.status == TransactionStatus.completed)
    result = await session.execute(query)
    return result.scalars().fetchall()
