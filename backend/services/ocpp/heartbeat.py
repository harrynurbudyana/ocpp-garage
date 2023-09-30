from ocpp.v16.call_result import HeartbeatPayload
from ocpp.v16.enums import ChargePointStatus

from core.utils import get_utc_as_string
from pyocpp_contrib.v16.views.events import HeartbeatCallEvent
from pyocpp_contrib.v16.views.tasks import HeartbeatCallResultTask
from services.charge_points import update_charge_point
from views.charge_points import ChargePointUpdateStatusView


async def process_heartbeat(session, event: HeartbeatCallEvent) -> HeartbeatCallResultTask:
    data = ChargePointUpdateStatusView(status=ChargePointStatus.available)
    await update_charge_point(session, event.charge_point_id, data=data)

    payload = HeartbeatPayload(current_time=get_utc_as_string())
    return HeartbeatCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
