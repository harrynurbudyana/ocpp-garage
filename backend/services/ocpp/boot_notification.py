from ocpp.v16.call_result import BootNotificationPayload
from ocpp.v16.enums import RegistrationStatus
from pyocpp_contrib.v16.views.events import BootNotificationCallEvent
from pyocpp_contrib.v16.views.tasks import BootNotificationCallResultTask

from core.utils import get_utc_as_string
from services.charge_points import get_charge_point


async def process_boot_notification(
        session,
        event: BootNotificationCallEvent
) -> BootNotificationCallResultTask:
    charge_point = await get_charge_point(session, event.charge_point_id)
    charge_point.model = event.payload.charge_point_model
    charge_point.vendor = event.payload.charge_point_vendor
    charge_point.serial_number = event.payload.charge_point_serial_number
    session.add(charge_point)
    
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
