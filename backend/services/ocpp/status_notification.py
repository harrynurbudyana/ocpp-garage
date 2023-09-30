from ocpp.v16.call_result import StatusNotificationPayload
from sqlalchemy.ext.asyncio import AsyncSession

from pyocpp_contrib.v16.views.events import StatusNotificationCallEvent
from pyocpp_contrib.v16.views.tasks import StatusNotificationCallResultTask
from services.charge_points import update_connectors


async def process_status_notification(
        session: AsyncSession,
        event: StatusNotificationCallEvent
) -> StatusNotificationCallResultTask:
    await update_connectors(session, event)
    payload = StatusNotificationPayload()

    return StatusNotificationCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
