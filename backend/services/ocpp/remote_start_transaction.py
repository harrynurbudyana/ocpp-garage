from uuid import uuid4

from ocpp.v16.call import RemoteStartTransactionPayload
from ocpp.v16.enums import ChargePointStatus
from pyocpp_contrib.v16.views.tasks import RemoteStartTransactionCallTask

from services.charge_points import get_charge_point


async def process_remote_start_transaction(
        session,
        charge_point_id: str,
        connector_id: int,
        id_tag: str
):
    charge_point = await get_charge_point(session, charge_point_id)
    charge_point.update_connector(session, connector_id, dict(status=ChargePointStatus.preparing))

    payload = RemoteStartTransactionPayload(
        connector_id=connector_id,
        id_tag=id_tag
    )
    return RemoteStartTransactionCallTask(
        charge_point_id=charge_point_id,
        payload=payload
    )
