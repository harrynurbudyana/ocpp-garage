from loguru import logger
from ocpp.v16.call import UnlockConnectorPayload
from ocpp.v16.enums import Action, UnlockStatus
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from pyocpp_contrib.v16.views.events import UnlockConnectorCallResultEvent
from services.actions import extend_actions_list, update_actions_status
from services.charge_points import get_charge_point_or_404
from views.actions import ActionView


@contextable
@send_call(Action.UnlockConnector)
async def process_unlock_connector(
        session: AsyncSession,
        charge_point_id: str,
        connector_id: int,
        message_id: str
) -> UnlockConnectorPayload:
    payload = UnlockConnectorPayload(
        connector_id=connector_id
    )
    logger.info(
        f"UnlockConnector -> | prepared payload={payload} (charge_point_id={charge_point_id}, connector_id={connector_id})")

    charge_point = await get_charge_point_or_404(session, charge_point_id)

    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point_id,
        connector_id=connector_id,
        body=f"Unlock connector"
    )
    await extend_actions_list(charge_point.garage_id, action)

    return payload


@use_context
async def process_unlock_connector_call_result(
        session: AsyncSession,
        event: UnlockConnectorCallResultEvent,
        context: UnlockConnectorPayload | None = None
):
    logger.info(f"<- UnlockConnector | start process call result response (event={event}, context={context})")
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)

    status = TransactionStatus.completed
    if UnlockStatus(event.payload.status) is not UnlockStatus.unlocked:
        status = TransactionStatus.faulted
    await update_actions_status(charge_point.garage_id, event.message_id, status=status)
