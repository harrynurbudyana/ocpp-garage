from ocpp.v16.call_result import SecurityEventNotificationPayload
from sqlalchemy.ext.asyncio import AsyncSession

from ocpp.v16.enums import Action
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import SecurityEventNotificationCallEvent


@response_call_result(Action.SecurityEventNotification)
async def process_security_event_notification(
        session: AsyncSession,
        event: SecurityEventNotificationCallEvent
) -> SecurityEventNotificationPayload:
    return SecurityEventNotificationPayload()
