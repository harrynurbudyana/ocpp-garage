from loguru import logger
from ocpp.v16.call import ResetPayload
from ocpp.v16.enums import ResetType, Action, ResetStatus, ChargePointStatus

from core.cache import ActionCache
from core.fields import TransactionStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from services.charge_points import get_charge_point, update_charge_point, update_connector
from services.transactions import get_active_transaction
from views.actions import ActionView
from views.charge_points import ChargePointUpdateStatusView


async def after_reset(message_id, charge_point):
    cache = ActionCache()
    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point.id,
        body="Reset station"
    )
    await cache.insert(charge_point.garage_id, action)


@contextable
@send_call(Action.Reset)
async def process_reset(
        session,
        charge_point_id: str,
        message_id: str,
        callback=after_reset
) -> ResetPayload:
    payload = ResetPayload(type=ResetType.soft)
    logger.info(f"Reset -> | prepared payload={payload}")

    if callback:
        charge_point = await get_charge_point(session, charge_point_id)
        await callback(message_id, charge_point)

    return payload


@use_context
async def process_reset_call_result(
        session,
        event,
        context: ResetPayload | None = None
):
    logger.info(f"<- Reset | start process call result response (event={event}, context={context})")
    cache = ActionCache()

    charge_point = await get_charge_point(session, event.charge_point_id)

    # After every server startup, the platfrom set all stations as unavailable.
    data = ChargePointUpdateStatusView(status=ChargePointStatus.available)
    await update_charge_point(session, charge_point_id=charge_point.id, data=data)

    if ResetStatus(event.payload.status) is ResetStatus.accepted:
        # Soft reset station can be requested after server startup
        # We need to ensure that station is not charging
        active_transaction = await get_active_transaction(session, event.charge_point_id)
        for connector in charge_point.connectors:
            if active_transaction and active_transaction.connector == connector.id:
                status = ChargePointStatus.charging
            else:
                status = ChargePointStatus.preparing
            data = ChargePointUpdateStatusView(status=status)
            await update_connector(session, charge_point_id=charge_point.id, connector_id=connector.id, data=data)
        await cache.update_status(charge_point.garage_id, event.message_id, status=TransactionStatus.completed)
        logger.info(f"<- Reset | refused reset by station (event={event}, context={context})")

    if ResetStatus(event.payload.status) is ResetStatus.rejected:
        await cache.update_status(charge_point.garage_id, event.message_id, status=TransactionStatus.faulted)
