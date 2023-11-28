from loguru import logger
from ocpp.v16.call import RemoteStartTransactionPayload
from ocpp.v16.enums import ChargePointStatus, Action, RemoteStartStopStatus

from core.cache import ActionCache
from core.fields import TransactionStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from services.charge_points import get_charge_point, update_connector
from views.actions import ActionView
from views.charge_points import ChargePointUpdateStatusView


@contextable
@send_call(Action.RemoteStartTransaction)
async def process_remote_start_transaction_call(
        session,
        charge_point_id: str,
        connector_id: int,
        id_tag: str,
        message_id: str
) -> RemoteStartTransactionPayload:
    charge_point = await get_charge_point(session, charge_point_id)
    logger.info(
        f"RemoteStartTransaction -> | Found charge point (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")
    data = ChargePointUpdateStatusView(status=ChargePointStatus.preparing)
    await update_connector(session, charge_point_id, connector_id, data)
    logger.info(
        f"RemoteStartTransaction -> | Updated connector with data={data} (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")
    payload = RemoteStartTransactionPayload(
        connector_id=connector_id,
        id_tag=id_tag
    )
    logger.info(
        f"RemoteStartTransaction -> | Prepared payload={payload} (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")

    cache = ActionCache()
    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point_id,
        connector_id=connector_id,
        body=f"Start transaction"
    )
    await cache.insert(charge_point.garage_id, action)

    return payload


@use_context
async def process_remote_start_transaction_call_result(
        session,
        event,
        context: RemoteStartTransactionPayload | None = None
):
    logger.info(f"<- RemoteStartTransaction | Start process call result response (event={event}, context={context}.)")
    cache = ActionCache()
    charge_point = await get_charge_point(session, event.charge_point_id)

    if RemoteStartStopStatus(event.payload.status) is RemoteStartStopStatus.accepted:
        await cache.update_status(charge_point.garage_id, event.message_id, status=TransactionStatus.completed)
    else:
        await cache.update_status(charge_point.garage_id, event.message_id, status=TransactionStatus.faulted)
        data = ChargePointUpdateStatusView(status=ChargePointStatus.available)
        await update_connector(session, event.charge_point_id, context.connector_id, data)
