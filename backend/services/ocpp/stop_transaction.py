from dataclasses import asdict

from ocpp.v16.call_result import StopTransactionPayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import AuthorizationStatus

from pyocpp_contrib.v16.views.events import StopTransactionCallEvent
from pyocpp_contrib.v16.views.tasks import StopTransactionCallResultTask
from services.transactions import update_transaction
from views.transactions import UpdateTransactionView


async def process_stop_transaction(
        session,
        event: StopTransactionCallEvent
) -> StopTransactionCallResultTask:
    view = UpdateTransactionView(
        transaction_id=event.payload.transaction_id,
        meter_stop=event.payload.meter_stop
    )
    await update_transaction(session, event.payload.transaction_id, view)

    payload = StopTransactionPayload(
        id_tag_info=asdict(IdTagInfo(status=AuthorizationStatus.accepted))
    )
    return StopTransactionCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
