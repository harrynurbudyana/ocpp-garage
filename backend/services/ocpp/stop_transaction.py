from dataclasses import asdict

from loguru import logger
from ocpp.v16.call_result import StopTransactionPayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import Action
from ocpp.v16.enums import AuthorizationStatus, ChargePointStatus
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import StopTransactionCallEvent
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from services.charge_points import update_connector
from services.transactions import update_transaction, get_transaction_or_404
from views.charge_points import UpdateChargPointView
from views.transactions import UpdateTransactionView


@response_call_result(Action.StopTransaction)
async def process_stop_transaction(
        session: AsyncSession,
        event: StopTransactionCallEvent
) -> StopTransactionPayload:
    logger.info(f"StopTransaction -> | start process call event (event={event})")

    view = UpdateTransactionView(
        meter_stop=event.payload.meter_stop
    )
    await update_transaction(session, event.payload.transaction_id, view)

    transaction = await get_transaction_or_404(session, event.payload.transaction_id)
    transaction.status = TransactionStatus.completed

    logger.info(f"StopTransaction -> | mark transaction as completed (event={event})")

    data = UpdateChargPointView(status=ChargePointStatus.available)
    await update_connector(
        session,
        event.charge_point_id,
        transaction.connector,
        data
    )
    logger.info(f"StopTransaction -> | mark connector as available (event={event})")
    payload = StopTransactionPayload(
        id_tag_info=asdict(IdTagInfo(status=AuthorizationStatus.accepted))
    )
    logger.info(f"StopTransaction -> | prepared payload={payload} (event={event})")
    return payload
