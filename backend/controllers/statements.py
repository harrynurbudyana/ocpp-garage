from typing import Tuple

from fastapi import Depends, Request
from starlette import status

from core.database import get_contextual_session
from models import Statement, Driver
from routers import AuthenticatedRouter
from services.statements import build_statements_query
from utils import params_extractor, paginate
from views.statements import PaginatedStatementsView

statements_router = AuthenticatedRouter(
    prefix="/{garage_id}/statements",
    tags=["statements"]
)


@statements_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_charge_points(
        garage_id: str,
        request: Request,
        search: str = "",
        params: Tuple = Depends(params_extractor)
) -> PaginatedStatementsView:
    async with get_contextual_session() as session:
        criterias = [
            Statement.driver_id == request.state.user.id,
            Driver.garage_id == garage_id
        ]
        items, pagination = await paginate(
            session,
            lambda: build_statements_query(search, extra_criterias=criterias),
            *params
        )
        return PaginatedStatementsView(items=[item[0] for item in items], pagination=pagination)
