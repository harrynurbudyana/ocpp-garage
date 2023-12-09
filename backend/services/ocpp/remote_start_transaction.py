from loguru import logger
from ocpp.v16.call import RemoteStartTransactionPayload
from ocpp.v16.enums import ChargePointStatus, Action, RemoteStartStopStatus
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from pyocpp_contrib.v16.views.events import RemoteStartTransactionCallResultEvent
from services.actions import extend_actions_list, update_actions_status
from services.charge_points import get_charge_point_or_404, update_connector
from views.actions import ActionView
from views.charge_points import UpdateChargPointView


@contextable
@send_call(Action.RemoteStartTransaction)
async def process_remote_start_transaction_call(
        session: AsyncSession,
        charge_point_id: str,
        connector_id: int,
        id_tag: str,
        message_id: str
) -> RemoteStartTransactionPayload:
    charge_point = await get_charge_point_or_404(session, charge_point_id)
    logger.info(
        f"RemoteStartTransaction -> | Found charge point (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")
    data = UpdateChargPointView(status=ChargePointStatus.preparing)
    await update_connector(session, charge_point_id, connector_id, data)
    logger.info(
        f"RemoteStartTransaction -> | Updated connector with data={data} (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")
    payload = RemoteStartTransactionPayload(
        connector_id=connector_id,
        id_tag=id_tag
    )
    logger.info(
        f"RemoteStartTransaction -> | Prepared payload={payload} (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")

    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point_id,
        connector_id=connector_id,
        body=f"Start transaction"
    )
    await extend_actions_list(charge_point.garage_id, action)

    return payload


@use_context
async def process_remote_start_transaction_call_result(
        session: AsyncSession,
        event: RemoteStartTransactionCallResultEvent,
        context: RemoteStartTransactionPayload | None = None
):
    logger.info(f"<- RemoteStartTransaction | Start process call result response (event={event}, context={context}.)")
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)

    if RemoteStartStopStatus(event.payload.status) is RemoteStartStopStatus.accepted:
        await update_actions_status(charge_point.garage_id, event.message_id, status=TransactionStatus.completed)
    else:
        await update_actions_status(charge_point.garage_id, event.message_id, status=TransactionStatus.faulted)
        data = UpdateChargPointView(status=ChargePointStatus.available)
        await update_connector(session, event.charge_point_id, context.connector_id, data)
