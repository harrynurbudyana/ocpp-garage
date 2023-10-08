from loguru import logger
from ocpp.v16.call import RemoteStopTransactionPayload
from ocpp.v16.enums import Action

from core.fields import TransactionStatus
from models import Transaction
from pyocpp_contrib.decorators import send_call, contextable, use_context


@contextable
@send_call(Action.RemoteStopTransaction)
async def process_remote_stop_transaction_call(
        session,
        charge_point_id: str,
        transaction: Transaction
) -> RemoteStopTransactionPayload:
    transaction.status = TransactionStatus.pending
    logger.info(
        f"RemoteStopTransaction -> | updated transactions status={transaction.status} (charge_point_id={charge_point_id}, transaction={transaction})")
    payload = RemoteStopTransactionPayload(transaction_id=transaction.transaction_id)
    logger.info(
        f"RemoteStopTransaction -> | prepared payload={payload} (charge_point_id={charge_point_id}, transaction={transaction})")
    return payload


@use_context
async def process_remote_stop_transaction_call_result(
        session,
        event,
        context: RemoteStopTransactionPayload | None
):
    logger.info(
        f"<- RemoteStopTransaction | start process response from the station (event={event}, context={context}.)")
