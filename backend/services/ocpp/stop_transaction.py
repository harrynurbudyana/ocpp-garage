from dataclasses import asdict

from ocpp.v16.call_result import StopTransactionPayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import Action
from ocpp.v16.enums import AuthorizationStatus, ChargePointStatus
from pyocpp_contrib.decorators import response_call_result

from core.fields import TransactionStatus
from services.charge_points import get_charge_point
from services.transactions import update_transaction, get_transaction
from views.transactions import UpdateTransactionView


@response_call_result(Action.StopTransaction)
async def process_stop_transaction(session, event) -> StopTransactionPayload:
    view = UpdateTransactionView(
        transaction_id=event.payload.transaction_id,
        meter_stop=event.payload.meter_stop
    )
    await update_transaction(session, event.payload.transaction_id, view)

    transaction = await get_transaction(session, event.payload.transaction_id)
    transaction.status = TransactionStatus.completed
    charge_point = await get_charge_point(session, event.charge_point_id)
    charge_point.update_connector(
        session,
        transaction.connector,
        dict(status=ChargePointStatus.available)
    )

    return StopTransactionPayload(
        id_tag_info=asdict(IdTagInfo(status=AuthorizationStatus.accepted))
    )
