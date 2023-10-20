from typing import List

from starlette import status

from core.database import get_contextual_session
from core.settings import NORDPOOL_REGION
from routers import AuthenticatedRouter
from services.grid_providers import retrieve_grid_providers
from views.grid_providers import SimpleGridProviderView

grid_providers_router = AuthenticatedRouter(
    prefix="/grid-providers",
    tags=["grid_providers"]
)


@grid_providers_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[SimpleGridProviderView]
)
async def list_grid_providers(search: str = ""):
    async with get_contextual_session() as session:
        return await retrieve_grid_providers(session, NORDPOOL_REGION, search)
