from loguru import logger
from ocpp.v16.call_result import MeterValuesPayload
from ocpp.v16.datatypes import SampledValue
from ocpp.v16.enums import Action, UnitOfMeasure
from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import MeterValuesCallEvent
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from services.transactions import update_transaction
from views.transactions import UpdateTransactionView


@response_call_result(Action.MeterValues)
async def process_meter_values(
        session: AsyncSession,
        event: MeterValuesCallEvent
) -> MeterValuesPayload:
    logger.info(f"Start process meter values (charge_point={event.charge_point_id}, payload={event.payload})")
    if event.payload.transaction_id:
        for meter_value in event.payload.meter_value or []:
            for sampled_value in meter_value.get("sampled_value", []):
                """
                Possible values sample:
                
                [
                    {
                        'context': 'Sample.Periodic',
                        'location': 'EV',
                        'measurand': 'SoC',
                        'unit': 'Percent',
                        'value': '9'
                    },
                    {
                        'context': 'Sample.Periodic',
                        'measurand': 'Voltage',
                        'unit': 'V',
                        'value': '419.9'
                    },
                    {
                        'context': 'Sample.Periodic',
                        'measurand': 'Power.Active.Import',
                        'unit': 'W',
                        'value': '10897.42'
                    },
                    {
                        'context': 'Sample.Periodic',
                        'measurand': 'Current.Import',
                        'unit': 'A',
                        'value': '30.04'
                    },
                    {
                        'context': 'Sample.Periodic', 
                        'unit': 'Wh', 
                        'value': '1545.31'
                    }
                ]
                """
                meter = SampledValue(**sampled_value)
                if meter.unit and UnitOfMeasure(meter.unit) is not UnitOfMeasure.wh:
                    continue
                try:
                    data = UpdateTransactionView(meter_stop=meter.value,
                                                 status=TransactionStatus.in_progress)
                except TypeError:
                    continue
                await update_transaction(session, event.payload.transaction_id, data)
    return MeterValuesPayload()
