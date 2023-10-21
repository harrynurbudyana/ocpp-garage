from typing import Tuple, List

from fastapi import status, Depends
from loguru import logger

from core.database import get_contextual_session
from routers import AuthenticatedRouter
from services.garages import build_garages_query, create_garage, list_simple_garages, get_garage, store_rates
from utils import params_extractor, paginate
from views.garages import PaginatedGaragesView, SingleGarageView, CreateGarageView, NotPaginatedSimpleGarageView, \
    SingleGarageWithProviderView, GarageRatesView, StoreSettingsView

garages_router = AuthenticatedRouter(
    prefix="/garages",
    tags=["garages"]
)


@garages_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def list_garages(
        search: str = "",
        params: Tuple = Depends(params_extractor),
) -> PaginatedGaragesView:
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_garages_query(search),
            *params
        )
        return PaginatedGaragesView(items=[item[0] for item in items], pagination=pagination)


@garages_router.get(
    "/{garage_id}",
    status_code=status.HTTP_200_OK,
    response_model=SingleGarageWithProviderView
)
async def retrieve_garage(garage_id: str):
    async with get_contextual_session() as session:
        return await get_garage(session, garage_id)


@garages_router.get(
    "/autocomplete",
    status_code=status.HTTP_200_OK,
    response_model=List[NotPaginatedSimpleGarageView]
)
async def retrieve_simple_garages():
    async with get_contextual_session() as session:
        return await list_simple_garages(session)


@garages_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SingleGarageView
)
async def add_garage(
        data: CreateGarageView
):
    logger.info(f"Start create garage (data={data})")
    async with get_contextual_session() as session:
        garage = await create_garage(session, data)
        await session.commit()
        return garage


@garages_router.get(
    "/{garage_id}/rates",
    status_code=status.HTTP_200_OK,
    response_model=GarageRatesView
)
async def get_garage_rates(garage_id: str):
    async with get_contextual_session() as session:
        garage = await get_garage(session, garage_id)
        return dict(
            daily=dict(garage_rate=garage.daily_rate, provider_rate=garage.grid_provider.daily_rate),
            nightly=dict(garage_rate=garage.nightly_rate, provider_rate=garage.grid_provider.nightly_rate)
        )


@garages_router.post(
    "/{garage_id}/settings",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def store_settings(
        garage_id: str,
        data: StoreSettingsView
):
    logger.info(f"Accepted settings for storing ({data.rates})")
    async with get_contextual_session() as session:
        await store_rates(session, garage_id, data.rates)
        await session.commit()
