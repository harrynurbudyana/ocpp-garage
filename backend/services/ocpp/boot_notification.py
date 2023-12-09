from ocpp.v16.call_result import BootNotificationPayload
from ocpp.v16.enums import RegistrationStatus, Action
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import BootNotificationCallEvent

from core.utils import get_utc_as_string
from services.charge_points import get_charge_point_or_404


@response_call_result(Action.BootNotification)
async def process_boot_notification(
        session: AsyncSession,
        event: BootNotificationCallEvent
) -> BootNotificationPayload:
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)
    charge_point.model = event.payload.charge_point_model
    charge_point.vendor = event.payload.charge_point_vendor
    charge_point.serial_number = event.payload.charge_point_serial_number
    session.add(charge_point)

    return BootNotificationPayload(
        current_time=get_utc_as_string(),
        interval=settings.HEARTBEAT_INTERVAL,
        status=RegistrationStatus.accepted
    )
