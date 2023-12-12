from loguru import logger
from ocpp.v16.call import RemoteStopTransactionPayload
from ocpp.v16.enums import Action, RemoteStartStopStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from pyocpp_contrib.v16.views.events import RemoteStopTransactionCallResultEvent
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from models import Transaction
from services.actions import extend_actions_list, update_actions_status
from services.charge_points import get_charge_point_or_404
from views.actions import ActionView


@contextable
@send_call(Action.RemoteStopTransaction)
async def process_remote_stop_transaction_call(
        session: AsyncSession,
        charge_point_id: str,
        transaction: Transaction,
        message_id: str
) -> RemoteStopTransactionPayload:
    payload = RemoteStopTransactionPayload(transaction_id=transaction.id)
    charge_point = await get_charge_point_or_404(session, charge_point_id)

    logger.info(
        f"RemoteStopTransaction -> | prepared payload={payload} (charge_point_id={charge_point_id})")

    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point_id,
        body=f"Stop transaction"
    )
    await extend_actions_list(charge_point.garage_id, action)

    return payload


@use_context
async def process_remote_stop_transaction_call_result(
        session: AsyncSession,
        event: RemoteStopTransactionCallResultEvent,
        context: RemoteStopTransactionPayload | None
):
    logger.info(
        f"<- RemoteStopTransaction | start process response from the station (event={event}, context={context}.)")
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)

    status = TransactionStatus.completed
    if RemoteStartStopStatus(event.payload.status) is not RemoteStartStopStatus.accepted:
        status = TransactionStatus.faulted
    await update_actions_status(charge_point.garage_id, event.message_id, status=status)
