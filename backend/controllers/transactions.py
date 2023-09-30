from typing import Tuple

from fastapi import Depends, Request
from loguru import logger
from starlette import status

from core.database import get_contextual_session
from pyocpp_contrib.queue.publisher import publish
from routers import AuthenticatedRouter
from services.ocpp.remote_start_transaction import process_remote_start_transaction
from services.transactions import build_transactions_query
from utils import params_extractor, paginate
from views.transactions import PaginatedTransactionsView

transactions_router = AuthenticatedRouter(prefix="/transactions", tags=["transactions"])


@transactions_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_transactions(
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedTransactionsView:
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_transactions_query(search),
            *params
        )
        return PaginatedTransactionsView(items=[item[0] for item in items], pagination=pagination)


@transactions_router.post(
    "/{charge_point_id}/connectors/{connector_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remote_start_transaction(
        charge_point_id: str,
        connector_id: int,
        request: Request
):
    logger.info(f"Start create new transaction (charge_point_id={charge_point_id}, connector_id={connector_id})")
    task = await process_remote_start_transaction(
        charge_point_id,
        connector_id,
        request.state.operator.id
    )
    await publish(task.json(), to=task.exchange, priority=task.priority)
