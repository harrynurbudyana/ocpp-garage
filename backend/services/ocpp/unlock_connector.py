from loguru import logger
from ocpp.v16.call import UnlockConnectorPayload
from ocpp.v16.enums import Action, UnlockStatus

from core.cache import ActionCache
from core.fields import TransactionStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from services.charge_points import get_charge_point
from views.actions import ActionView


@contextable
@send_call(Action.UnlockConnector)
async def process_unlock_connector(
        session,
        charge_point_id: str,
        connector_id: int,
        message_id: str
) -> UnlockConnectorPayload:
    payload = UnlockConnectorPayload(
        connector_id=connector_id
    )
    logger.info(
        f"UnlockConnector -> | prepared payload={payload} (charge_point_id={charge_point_id}, connector_id={connector_id})")

    charge_point = await get_charge_point(session, None, charge_point_id)

    cache = ActionCache()
    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point_id,
        body=f"Unlock connector ({connector_id})"
    )
    await cache.insert(charge_point.garage_id, action)

    return payload


@use_context
async def process_unlock_connector_call_result(
        session,
        event,
        context: UnlockConnectorPayload | None = None
):
    logger.info(f"<- UnlockConnector | start process call result response (event={event}, context={context})")
    cache = ActionCache()
    charge_point = await get_charge_point(session, None, event.charge_point_id)

    if UnlockStatus(event.payload.status) is UnlockStatus.unlocked:
        await cache.update_status(charge_point.garage_id, event.message_id, status=TransactionStatus.completed)
    else:
        await cache.update_status(charge_point.garage_id, event.message_id, status=TransactionStatus.faulted)
