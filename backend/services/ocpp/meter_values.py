from ocpp.v16.call_result import MeterValuesPayload

from pyocpp_contrib.v16.views.events import MeterValuesCallEvent
from pyocpp_contrib.v16.views.tasks import MeterValuesCallResultTask


async def process_meter_values(
        session,
        event: MeterValuesCallEvent
) -> MeterValuesCallResultTask:
    payload = MeterValuesPayload()
    return MeterValuesCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
