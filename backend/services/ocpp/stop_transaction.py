from dataclasses import asdict

from loguru import logger
from ocpp.v16.call_result import StopTransactionPayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import Action
from ocpp.v16.enums import AuthorizationStatus, ChargePointStatus
from pyocpp_contrib.decorators import response_call_result

from core.fields import TransactionStatus
from services.charge_points import update_connector, get_connector
from services.transactions import update_transaction, get_transaction
from views.charge_points import ChargePointUpdateStatusView
from views.transactions import UpdateTransactionView


@response_call_result(Action.StopTransaction)
async def process_stop_transaction(session, event) -> StopTransactionPayload:
    logger.info(f"StopTransaction -> | start process call event (event={event})")

    view = UpdateTransactionView(
        transaction_id=event.payload.transaction_id,
        meter_stop=event.payload.meter_stop
    )
    await update_transaction(session, event.payload.transaction_id, view)

    transaction = await get_transaction(session, event.payload.transaction_id)
    transaction.status = TransactionStatus.completed

    connector = await get_connector(session, event.charge_point_id, transaction.connector)
    logger.info(f"StopTransaction -> | mark transaction as completed (event={event}, driver={connector.driver})")

    data = ChargePointUpdateStatusView(status=ChargePointStatus.available)
    await update_connector(
        session,
        event.charge_point_id,
        transaction.connector,
        data
    )
    logger.info(f"StopTransaction -> | mark connector as available (event={event}, driver={connector.driver})")
    payload = StopTransactionPayload(
        id_tag_info=asdict(IdTagInfo(status=AuthorizationStatus.accepted))
    )
    logger.info(f"StopTransaction -> | prepared payload={payload} (event={event}, driver={connector.driver})")
    return payload
