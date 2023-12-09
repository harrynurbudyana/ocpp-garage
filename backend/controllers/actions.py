from typing import List

from fastapi import status

from routers import AuthenticatedRouter
from views.actions import ActionView
from services.actions import get_all_actions

private_router = AuthenticatedRouter(
    prefix="/actions",
    tags=["actions"]
)


@private_router.get(
    "/{garage_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[ActionView]
)
async def list_actions(garage_id):
    return await get_all_actions(garage_id)
