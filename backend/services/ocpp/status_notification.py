from pyocpp_contrib.v16.views.events import StatusNotificationEvent
from pyocpp_contrib.v16.views.tasks import StatusNotificationResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.charge_points import update_connectors


async def process_status_notification(
        session: AsyncSession,
        event: StatusNotificationEvent
) -> StatusNotificationResponse:
    await update_connectors(session, event)

    return StatusNotificationResponse(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id
    )
