from __future__ import annotations

from typing import List

from pyocpp_contrib.cache import get_connection
from sqlalchemy import update, select, or_, func, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable

from core import settings
from core.fields import TransactionStatus
from exceptions import NotFound
from models import Transaction
from views.transactions import CreateTransactionView, UpdateTransactionView


def _make_key_for_cache(charge_point_id: str, connector_id: int) -> str:
    return f"{charge_point_id}_{connector_id}"


async def memorize_track_id(charge_point_id: str, connector_id: int, track_id: str):
    # We need a track id before the transaction to be created.
    connection = await get_connection()
    key = _make_key_for_cache(charge_point_id, connector_id)
    await connection.set(key, track_id)
    await connection.expire(key, settings.TRANSACTION_TRACK_ID_EXPIRE_AFTER)


async def recall_track_id_or_404(charge_point_id: str, connector_id: int) -> str:
    connection = await get_connection()
    key = _make_key_for_cache(charge_point_id, connector_id)
    context: bytes | None = await connection.get(key)
    try:
        track_id = context.decode()
        await connection.delete(key)
    except AttributeError:
        track_id = None
    if not track_id:
        raise NotFound
    return track_id


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
        id: int | str
) -> Transaction:
    expr = select(Transaction)
    if isinstance(id, int):
        query = await session.execute(expr.where(Transaction.id == id))
    if isinstance(id, str):
        query = await session.execute(expr.where(Transaction.track_id == id))
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
