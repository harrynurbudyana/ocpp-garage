from ocpp.v16.call_result import HeartbeatPayload
from ocpp.v16.enums import Action
from ocpp.v16.enums import ChargePointStatus
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import get_utc_as_string
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import HeartbeatCallEvent
from services.charge_points import update_charge_point
from views.charge_points import UpdateChargPointView


@response_call_result(Action.Heartbeat)
async def process_heartbeat(
        session: AsyncSession,
        event: HeartbeatCallEvent
) -> HeartbeatPayload:
    data = UpdateChargPointView(status=ChargePointStatus.available)
    await update_charge_point(session, event.charge_point_id, data=data)

    return HeartbeatPayload(current_time=get_utc_as_string())
