from ocpp.v16.call_result import SecurityEventNotificationPayload

from pyocpp_contrib.v16.views.events import SecurityEventNotificationCallEvent
from pyocpp_contrib.v16.views.tasks import SecurityEventNotificationCallResultTask


async def process_security_event_notification(
        session,
        event: SecurityEventNotificationCallEvent
) -> SecurityEventNotificationCallResultTask:
    payload = SecurityEventNotificationPayload()
    return SecurityEventNotificationCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
