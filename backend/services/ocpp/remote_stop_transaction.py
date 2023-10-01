from uuid import uuid4

from ocpp.v16.call import RemoteStopTransactionPayload
from pyocpp_contrib.v16.views.tasks import RemoteStopTransactionCallTask


async def process_remote_stop_transaction(charge_point_id: str, transaction_id: int):
    payload = RemoteStopTransactionPayload(transaction_id=transaction_id)
    return RemoteStopTransactionCallTask(
        message_id=str(uuid4()),
        charge_point_id=charge_point_id,
        payload=payload
    )
