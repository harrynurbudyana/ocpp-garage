from typing import List

from starlette import status

from core.database import get_contextual_session
from routers import AuthenticatedRouter
from services.grid_providers import retrieve_grid_providers
from views.grid_providers import SimpleGridProviderView

private_router = AuthenticatedRouter(
    prefix="/grid-providers",
    tags=["grid_providers"]
)


@private_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[SimpleGridProviderView]
)
async def list_grid_providers(search: str = ""):
    async with get_contextual_session() as session:
        return await retrieve_grid_providers(session, search)
