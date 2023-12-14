from dataclasses import asdict

from loguru import logger
from ocpp.v16.call_result import StartTransactionPayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import Action
from ocpp.v16.enums import AuthorizationStatus, ChargePointStatus
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import StartTransactionCallEvent
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import NotFound
from services.charge_points import (
    update_connector,
    get_connector_or_404
)
from services.transactions import create_transaction, recall_session_context_or_404
from views.charge_points import UpdateChargPointView
from views.transactions import CreateTransactionView


@response_call_result(Action.StartTransaction)
async def process_start_transaction(
        session: AsyncSession,
        event: StartTransactionCallEvent
) -> StartTransactionPayload:
    logger.info(f"StartTransaction -> | start process call event (event={event})")
    connector = await get_connector_or_404(session, event.charge_point_id, event.payload.connector_id)

    data = UpdateChargPointView(status=ChargePointStatus.charging)
    await update_connector(
        session,
        event.charge_point_id,
        event.payload.connector_id,
        data
    )
    try:
        track_id = await recall_session_context_or_404(event.charge_point_id, event.payload.connector_id)
        status = AuthorizationStatus.accepted
        logger.info(f"Successfully obtained track_id (event={event})")
    except NotFound:
        track_id = ""
        status = AuthorizationStatus.blocked
        logger.info(f"Could not create a new transaction due to expired track_id (event={event})")
    # It is a good practice to always create transaction
    view = CreateTransactionView(
        garage=connector.charge_point.garage.id,
        meter_start=event.payload.meter_start,
        charge_point=connector.charge_point.id,
        connector=connector.id,
        limit=connector.latest_limit,
        track_id=track_id
    )
    transaction = await create_transaction(session, view)
    await session.flush()

    logger.info(
        f"StartTransaction -> | created new transaction with data={view} (transaction={transaction})")

    payload = StartTransactionPayload(
        transaction_id=transaction.id,
        id_tag_info=asdict(IdTagInfo(status=status))
    )
    logger.info(
        f"StartTransaction -> | prepared payload={payload}, charge_point_id={connector.charge_point.id}")
    return payload
