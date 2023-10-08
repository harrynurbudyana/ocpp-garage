from loguru import logger
from ocpp.v16.call import ResetPayload
from ocpp.v16.enums import ResetType, Action, ResetStatus, ChargePointStatus

from pyocpp_contrib.decorators import send_call, contextable, use_context
from services.charge_points import get_charge_point


@contextable
@send_call(Action.Reset)
async def process_reset(charge_point_id: str) -> ResetPayload:
    payload = ResetPayload(type=ResetType.soft)
    logger.info(f"Reset -> | prepared payload={payload}")
    return payload


@use_context
async def process_reset_call_result(
        session,
        event,
        context: ResetPayload | None = None
):
    logger.info(f"<- Reset | start process call result response (event={event}, context={context})")
    if ResetStatus(event.payload.status) is ResetStatus.accepted:
        charge_point = await get_charge_point(session, event.charge_point_id)
        charge_point.connectors.clear()
        charge_point.status = ChargePointStatus.unavailable
        logger.info(f"<- Reset | refused reset by station (event={event}, context={context})")
