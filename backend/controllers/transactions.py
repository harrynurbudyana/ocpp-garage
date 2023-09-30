from typing import Tuple

from fastapi import Depends
from starlette import status

from core.database import get_contextual_session
from routers import AuthenticatedRouter
from services.transactions import build_transactions_query
from utils import params_extractor, paginate
from views.transactions import PaginatedTransactionsView

transactions_router = AuthenticatedRouter(prefix="/transactions", tags=["transactions"])


@transactions_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_charge_points(
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
