from ocpp.v16.call import RemoteStopTransactionPayload
from ocpp.v16.enums import Action
from pyocpp_contrib.decorators import send_call

from core.fields import TransactionStatus
from models import Transaction


@send_call(Action.RemoteStopTransaction)
async def process_remote_stop_transaction(
        session,
        charge_point_id: str,
        transaction: Transaction
) -> RemoteStopTransactionPayload:
    transaction.status = TransactionStatus.pending
    return RemoteStopTransactionPayload(transaction_id=transaction.transaction_id)
