from typing import Tuple

from fastapi import Depends, Request
from loguru import logger
from starlette import status

from core.database import get_contextual_session
from models import Transaction
from pyocpp_contrib.decorators import message_id_generator
from routers import AuthenticatedRouter
from services.ocpp.remote_start_transaction import process_remote_start_transaction_call
from services.ocpp.remote_stop_transaction import process_remote_stop_transaction_call
from services.transactions import build_transactions_query, get_transaction_or_404
from utils import params_extractor, paginate
from views.transactions import PaginatedTransactionsView, InitTransactionView

private_router = AuthenticatedRouter(prefix="/{garage_id}/transactions", tags=["transactions"])


@private_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_transactions(
        garage_id: str,
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedTransactionsView:
    criterias = [
        Transaction.garage == garage_id
    ]
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_transactions_query(search, extra_criterias=criterias),
            *params
        )
        return PaginatedTransactionsView(items=[item[0] for item in items], pagination=pagination)


@private_router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remote_start_transaction(
        garage_id: str,
        data: InitTransactionView,
        request: Request
):
    logger.info(f"RemoteStartTransaction -> | Start process call request (data={data})")
    async with get_contextual_session() as session:
        await process_remote_start_transaction_call(
            session,
            charge_point_id=data.charge_point_id,
            connector_id=data.connector_id,
            id_tag=request.state.user.id_tag,
            message_id=message_id_generator()
        )
        await session.commit()


@private_router.put(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remote_stop_transaction(garage_id, transaction_id: int):
    async with get_contextual_session() as session:
        transaction = await get_transaction_or_404(session, transaction_id)
        logger.info(f"RemoteStopTransaction -> | Start process call request (transaction={transaction})")
        await process_remote_stop_transaction_call(
            session,
            charge_point_id=transaction.charge_point,
            transaction=transaction,
            message_id=message_id_generator()
        )
        await session.commit()
