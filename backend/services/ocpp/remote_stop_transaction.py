from ocpp.v16.call import RemoteStopTransactionPayload
from pyocpp_contrib.v16.views.tasks import RemoteStopTransactionCallTask

from core.fields import TransactionStatus
from services.transactions import get_transaction


async def process_remote_stop_transaction(session, transaction_uuid: str):
    transaction = await get_transaction(session, transaction_uuid)
    transaction.status = TransactionStatus.pending
    payload = RemoteStopTransactionPayload(transaction_id=transaction.transaction_id)
    return RemoteStopTransactionCallTask(
        charge_point_id=transaction.charge_point,
        payload=payload
    )
