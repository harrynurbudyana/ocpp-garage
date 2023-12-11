from dataclasses import asdict

from loguru import logger
from ocpp.v16.call_result import StartTransactionPayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import Action
from ocpp.v16.enums import AuthorizationStatus, ChargePointStatus
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import StartTransactionCallEvent
from sqlalchemy.ext.asyncio import AsyncSession

from services.charge_points import (
    get_charge_point_or_404,
    update_connector,
    get_connector_or_404
)
from services.transactions import create_transaction
from views.charge_points import UpdateChargPointView
from views.transactions import CreateTransactionView


@response_call_result(Action.StartTransaction)
async def process_start_transaction(
        session: AsyncSession,
        event: StartTransactionCallEvent
) -> StartTransactionPayload:
    logger.info(f"StartTransaction -> | start process call event (event={event})")
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)
    connector = await get_connector_or_404(session, event.charge_point_id, event.payload.connector_id)
    # It is a good practice to always create transaction
    view = CreateTransactionView(
        garage=charge_point.garage.id,
        meter_start=event.payload.meter_start,
        charge_point=charge_point.id,
        connector=connector.id
    )
    data = UpdateChargPointView(status=ChargePointStatus.charging)
    await update_connector(
        session,
        event.charge_point_id,
        event.payload.connector_id,
        data
    )
    logger.info(
        f"StartTransaction -> | allowed charging (charge_point_id={charge_point.id}, connectors={charge_point.connectors})")

    transaction = await create_transaction(session, view)
    await session.flush()
    logger.info(
        f"StartTransaction -> | created new transaction with data={view} (charge_point_id={charge_point.id}, transaction={transaction})")

    payload = StartTransactionPayload(
        transaction_id=transaction.id,
        id_tag_info=asdict(IdTagInfo(status=AuthorizationStatus.accepted))
    )
    logger.info(
        f"StartTransaction -> | prepared payload={payload}, charge_point_id={charge_point.id}")
    return payload
