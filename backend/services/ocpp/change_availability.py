from ocpp.v16.call import ChangeAvailabilityPayload
from ocpp.v16.enums import AvailabilityType, Action, AvailabilityStatus, ChargePointStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context

from services.charge_points import get_charge_point


@contextable
@send_call(Action.ChangeAvailability)
async def process_change_availability(
        charge_point_id: str,
        connector_id: int,
        type: AvailabilityType
) -> ChangeAvailabilityPayload:
    return ChangeAvailabilityPayload(connector_id=connector_id, type=type)


@use_context
async def process_change_availability_call_result(
        session,
        event,
        context: ChangeAvailabilityPayload | None = None
):
    charge_point = await get_charge_point(session, event.charge_point_id)

    status = AvailabilityStatus(event.payload.status)
    if status is AvailabilityStatus.accepted and context:
        if not context.connector_id:
            charge_point.status = ChargePointStatus.available
        else:
            charge_point.update_connector(
                session,
                context.connector_id,
                dict(status=ChargePointStatus.available)
            )
    if status is AvailabilityStatus.scheduled:
        if context.connector_id and context:
            charge_point.update_connector(
                session,
                context.connector_id,
                dict(status=ChargePointStatus.charging)
            )
    if status is AvailabilityStatus.rejected:
        if not context.connector_id and context:
            charge_point.status = ChargePointStatus.unavailable
        else:
            charge_point.update_connector(
                session,
                context.connector_id,
                dict(status=ChargePointStatus.unavailable)
            )
