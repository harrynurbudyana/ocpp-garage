from ocpp.v16.call_result import StatusNotificationPayload
from ocpp.v16.enums import Action
from sqlalchemy.ext.asyncio import AsyncSession

from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import StatusNotificationCallEvent
from services.charge_points import create_or_update_connector, update_charge_point
from views.charge_points import UpdateChargPointView


@response_call_result(Action.StatusNotification)
async def process_status_notification(
        session: AsyncSession,
        event: StatusNotificationCallEvent
) -> StatusNotificationPayload:
    if not event.payload.connector_id:
        data = UpdateChargPointView(status=event.payload.status)
        await update_charge_point(session, event.charge_point_id, data)
    else:
        await create_or_update_connector(session, event)
    return StatusNotificationPayload()
