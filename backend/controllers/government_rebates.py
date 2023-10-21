from typing import Tuple

from fastapi import Depends
from loguru import logger
from starlette import status

from core.database import get_contextual_session
from models import GovernmentRebate
from routers import AuthenticatedRouter
from services.government_rebates import build_government_rebates_query, create_government_rebate, \
    update_government_rebate, remove_government_rebate
from utils import params_extractor, paginate
from views.government_rebates import PaginatedGovernmentRebatesView, CreateGovernmentRebateView, \
    UpdateGovernmentRebateView, ReadGovernmentRebateView

government_rebates_router = AuthenticatedRouter(
    prefix="/{garage_id}/government-rebates",
    tags=["government-rebates"]
)


@government_rebates_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def retrieve_government_rebates(
        garage_id: str,
        params: Tuple = Depends(params_extractor)
) -> PaginatedGovernmentRebatesView:
    criterias = [
        GovernmentRebate.garage_id == garage_id
    ]
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_government_rebates_query(criterias),
            *params
        )
        return PaginatedGovernmentRebatesView(items=[item[0] for item in items], pagination=pagination)


@government_rebates_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_government_rebate(
        garage_id: str,
        data: CreateGovernmentRebateView
):
    logger.info(f"Start create government rebate (data={data})")
    async with get_contextual_session() as session:
        await create_government_rebate(session, garage_id, data)
        await session.commit()


@government_rebates_router.put(
    "/{government_rebate_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ReadGovernmentRebateView
)
async def edit_government_rebate(
        garage_id: str,
        government_rebate_id: str,
        data: UpdateGovernmentRebateView
):
    logger.info(f"Start update government rebate (data={data})")
    async with get_contextual_session() as session:
        await update_government_rebate(session, garage_id, government_rebate_id, data)
        await session.commit()


@government_rebates_router.delete(
    "/{government_rebate_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_government_rebate(
        garage_id: str,
        government_rebate_id: str
):
    logger.info(f"Start remove government rebate (government_rebate_id={government_rebate_id})")
    async with get_contextual_session() as session:
        await remove_government_rebate(session, garage_id, government_rebate_id)
        await session.commit()
