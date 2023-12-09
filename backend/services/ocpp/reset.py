from loguru import logger
from ocpp.v16.call import ResetPayload
from ocpp.v16.enums import ResetType, Action, ResetStatus
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from pyocpp_contrib.decorators import send_call, contextable, use_context
from pyocpp_contrib.v16.views.events import ResetCallResultEvent
from services.actions import extend_actions_list, update_actions_status
from services.charge_points import get_charge_point_or_404
from views.actions import ActionView


async def after_reset(message_id, charge_point):
    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point.id,
        body="Reset station"
    )
    await extend_actions_list(charge_point.garage_id, action)


@contextable
@send_call(Action.Reset)
async def process_reset(
        session: AsyncSession,
        charge_point_id: str,
        message_id: str,
        callback=after_reset
) -> ResetPayload:
    payload = ResetPayload(type=ResetType.soft)
    logger.info(f"Reset -> | prepared payload={payload}")

    if callback:
        charge_point = await get_charge_point_or_404(session, charge_point_id)
        await callback(message_id, charge_point)

    return payload


@use_context
async def process_reset_call_result(
        session: AsyncSession,
        event: ResetCallResultEvent,
        context: ResetPayload | None = None
):
    logger.info(f"<- Reset | start process call result response (event={event}, context={context})")
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)

    status = TransactionStatus.completed
    if ResetStatus(event.payload.status) is not ResetStatus.accepted:
        status = TransactionStatus.faulted
    await update_actions_status(charge_point.garage_id, event.message_id, status=status)
