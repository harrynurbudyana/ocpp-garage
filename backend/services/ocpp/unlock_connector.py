from uuid import uuid4

from ocpp.v16.call import UnlockConnectorPayload
from pyocpp_contrib.v16.views.tasks import UnlockConnectorCallTask


async def process_unlock_connector(charge_point_id: str, connector_id: int) -> UnlockConnectorCallTask:
    payload = UnlockConnectorPayload(
        connector_id=connector_id
    )
    return UnlockConnectorCallTask(
        message_id=str(uuid4()),
        charge_point_id=charge_point_id,
        payload=payload
    )
