from loguru import logger
from ocpp.v16.call import RemoteStartTransactionPayload
from ocpp.v16.enums import ChargePointStatus, Action

from pyocpp_contrib.decorators import send_call, contextable, use_context
from services.charge_points import get_charge_point


@contextable
@send_call(Action.RemoteStartTransaction)
async def process_remote_start_transaction_call(
        session,
        charge_point_id: str,
        connector_id: int,
        id_tag: str
) -> RemoteStartTransactionPayload:
    charge_point = await get_charge_point(session, charge_point_id)
    await charge_point.update_connector(session, connector_id, dict(status=ChargePointStatus.preparing))
    return RemoteStartTransactionPayload(
        connector_id=connector_id,
        id_tag=id_tag
    )


@use_context
async def process_remote_start_transaction_call_result(
        session,
        event,
        context: RemoteStartTransactionPayload | None = None
):
    logger.info(f"Start process RemoteStartTransaction response from the station (event={event}, context={context}.)")
