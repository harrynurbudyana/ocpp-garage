from __future__ import annotations

from typing import List

from sqlalchemy import update, select, or_, func, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable

from core.fields import TransactionStatus
from exceptions import NotFound
from models import Transaction
from views.transactions import CreateTransactionView, UpdateTransactionView


async def create_transaction(
        session: AsyncSession,
        data: CreateTransactionView
) -> Transaction:
    transaction = Transaction(**data.dict())
    session.add(transaction)
    return transaction


async def update_transaction(
        session: AsyncSession,
        id: int,
        data: UpdateTransactionView
) -> None:
    await session.execute(
        update(Transaction) \
            .where(Transaction.id == id) \
            .values(**data.dict())
    )


async def cancel_in_progress_transactions(
        session: AsyncSession,
        charge_point_id: str,
        data: UpdateTransactionView
) -> None:
    await session.execute(
        update(Transaction) \
            .where(Transaction.charge_point == charge_point_id,
                   Transaction.status == TransactionStatus.in_progress) \
            .values(**data.dict())
    )


async def get_transaction_or_404(
        session: AsyncSession,
        id: int
) -> Transaction:
    query = await session.execute(
        select(Transaction).where(Transaction.id == id))
    transaction = query.scalars().first()
    if not transaction:
        raise NotFound(detail="The transaction is not found.")
    return transaction


async def build_transactions_query(
        search: str,
        extra_criterias: List | None = None
) -> selectable:
    query = select(Transaction)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(Transaction.id.desc())
    if search:
        query = query.where(or_(
            func.lower(Transaction.garage).contains(func.lower(search)),
            func.cast(Transaction.charge_point, String).ilike(f"{search}%"),
        ))
    return query
