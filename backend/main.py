import asyncio

from ocpp.v16.call import StatusNotificationPayload
from ocpp.v16.enums import AvailabilityType
from pyocpp_contrib.queue.consumer import start_consume
from pyocpp_contrib.queue.publisher import publish
from pyocpp_contrib.settings import EVENTS_EXCHANGE_NAME

from app import app
from controllers.charge_points import charge_points_router, anonymous_charge_points_router
from controllers.drivers import drivers_router
from controllers.operators import operators_public_router, operators_private_router
from controllers.transactions import transactions_router
from core.database import get_contextual_session
from events import process_event
from services.charge_points import list_simple_charge_points, reset_charge_points
from services.ocpp.change_availability import process_change_availability

background_tasks = set()


@app.on_event("startup")
async def startup():
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    task = asyncio.create_task(
        start_consume(exchange_name=EVENTS_EXCHANGE_NAME, on_message=process_event)
    )
    background_tasks.add(task)

    # Its possible that the manager does not work but standalone charge point nodes do.
    # Thus, everytime we start manager, we need to sync charge points statuses
    async with get_contextual_session() as session:
        await reset_charge_points(session)
        await session.commit()
        charge_points = await list_simple_charge_points(session, all=True)
        for charge_point in charge_points:
            task = await process_change_availability(
                charge_point_id=charge_point.id,
                # zero means whole station
                connector_id=0,
                type=AvailabilityType.operative
            )
            await publish(task.json(), to=task.exchange, priority=task.priority)
            # Iterate over connectors.
            for data in charge_point.connectors:
                connector = StatusNotificationPayload(**data)
                task = await process_change_availability(
                    charge_point_id=charge_point.id,
                    # zero means whole station
                    connector_id=connector.connector_id,
                    type=AvailabilityType.operative
                )
                await publish(task.json(), to=task.exchange, priority=task.priority)


app.include_router(transactions_router)
app.include_router(anonymous_charge_points_router)
app.include_router(drivers_router)
app.include_router(operators_public_router)
app.include_router(operators_private_router)
app.include_router(charge_points_router)
