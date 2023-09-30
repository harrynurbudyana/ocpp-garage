from ocpp.v16.call_result import BootNotificationPayload
from ocpp.v16.enums import RegistrationStatus

from core.utils import get_utc_as_string
from pyocpp_contrib.v16.views.events import BootNotificationCallEvent
from pyocpp_contrib.v16.views.tasks import BootNotificationCallResultTask


async def process_boot_notification(
        session,
        event: BootNotificationCallEvent
) -> BootNotificationCallResultTask:
    payload = BootNotificationPayload(
        current_time=get_utc_as_string(),
        interval=7200,
        status=RegistrationStatus.accepted
    )
    return BootNotificationCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
