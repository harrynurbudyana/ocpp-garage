from loguru import logger
from ocpp.v16.call import UnlockConnectorPayload
from ocpp.v16.enums import Action

from pyocpp_contrib.decorators import send_call, contextable, use_context


@contextable
@send_call(Action.UnlockConnector)
async def process_unlock_connector(
        charge_point_id: str,
        connector_id: int
) -> UnlockConnectorPayload:
    payload = UnlockConnectorPayload(
        connector_id=connector_id
    )
    logger.info(
        f"UnlockConnector -> | prepared payload={payload} (charge_point_id={charge_point_id}, connector_id={connector_id})")
    return payload


@use_context
async def process_unlock_connector_call_result(
        session,
        event,
        context: UnlockConnectorPayload | None = None
):
    logger.info(f"<- UnlockConnector | start process call result response (event={event}, context={context})")
