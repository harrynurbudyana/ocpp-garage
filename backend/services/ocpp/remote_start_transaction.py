from uuid import uuid4

from ocpp.v16.call import RemoteStartTransactionPayload

from pyocpp_contrib.v16.views.tasks import RemoteStartTransactionCallTask


async def process_remote_start_transaction(charge_point_id: str, connector_id: int, id_tag: str):
    payload = RemoteStartTransactionPayload(
        connector_id=connector_id,
        id_tag=id_tag
    )
    return RemoteStartTransactionCallTask(
        message_id=str(uuid4()),
        charge_point_id=charge_point_id,
        payload=payload
    )
