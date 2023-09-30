from dataclasses import asdict

from loguru import logger
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import AuthorizationStatus
from pyocpp_contrib.v16.views.events import StartTransactionEvent
from pyocpp_contrib.v16.views.tasks import StartTransactionResponse

from services.charge_points import get_charge_point
from services.transactions import create_transaction
from views.transactions import CreateTransactionView


async def process_start_transaction(
        session,
        event: StartTransactionEvent
) -> StartTransactionResponse:
    logger.info(f"Start process StartTransaction (event={event})")
    charge_point = await get_charge_point(session, event.charge_point_id)
    view = CreateTransactionView(
        driver=charge_point.driver.email,
        meter_start=event.payload.meter_start,
        charge_point=charge_point.id,
        connector=event.payload.connector_id
    )
    transaction = await create_transaction(session, view)
    await session.flush()

    return StartTransactionResponse(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        transaction_id=transaction.transaction_id,
        id_tag_info=asdict(IdTagInfo(status=AuthorizationStatus.accepted))
    )
