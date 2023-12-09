import asyncio

from loguru import logger

from app import app
from controllers.actions import (
    private_router as actions_private_router
)
from controllers.auth import (
    public_router as auth_public_router,
    private_router as auth_private_router
)
from controllers.charge_points import (
    public_router as charge_point_public_router,
    private_router as charge_point_private_router
)
from controllers.garages import (
    private_router as garages_private_router
)
from controllers.grid_providers import (
    private_router as grid_provider_private_router
)
from controllers.transactions import (
    private_router as transactions_private_router
)
from controllers.users import (
    private_router as users_private_router,
    public_router as users_public_router
)
from events import process_event
from pyocpp_contrib.decorators import init_logger
from pyocpp_contrib.queue.consumer import start_consume
from pyocpp_contrib.settings import EVENTS_EXCHANGE_NAME

background_tasks = set()


@app.on_event("startup")
async def startup():
    init_logger(logger)
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    task = asyncio.create_task(
        start_consume(exchange_name=EVENTS_EXCHANGE_NAME, on_message=process_event)
    )
    background_tasks.add(task)


app.include_router(grid_provider_private_router)

app.include_router(actions_private_router)

app.include_router(auth_public_router)
app.include_router(auth_private_router)

app.include_router(charge_point_public_router)
app.include_router(charge_point_private_router)

app.include_router(garages_private_router)

app.include_router(transactions_private_router)

app.include_router(users_private_router)
app.include_router(users_public_router)
