from loguru import logger
from ocpp.v16.call_result import MeterValuesPayload
from ocpp.v16.enums import Action

from pyocpp_contrib.decorators import response_call_result
from services.transactions import update_transaction
from views.transactions import UpdateTransactionView


@response_call_result(Action.MeterValues)
async def process_meter_values(session, event) -> MeterValuesPayload:
    logger.info(f"Start process meter values (charge_point={event.charge_point_id}, payload={event.payload})")
    if event.payload.transaction_id:
        for sampled_value in event.payload.meter_value or []:
            for meter in sampled_value.get("sampledValue", []) or sampled_value.get("sampled_value", []):
                value = meter.get("value")
                try:
                    value = int(value)
                    data = UpdateTransactionView(meter_stop=value)
                except TypeError:
                    continue
                await update_transaction(session, event.payload.transaction_id, data)
    return MeterValuesPayload()
