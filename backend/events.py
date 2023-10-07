from copy import deepcopy

from loguru import logger
from ocpp.v16.enums import Action, ChargePointStatus
from pyocpp_contrib.decorators import prepare_event
from pyocpp_contrib.enums import ConnectionAction

from core.database import get_contextual_session
from services.charge_points import update_charge_point, reset_connectors
from services.ocpp.authorize import process_authorize
from services.ocpp.boot_notification import process_boot_notification
from services.ocpp.change_configuration import init_configuration
from services.ocpp.heartbeat import process_heartbeat
from services.ocpp.meter_values import process_meter_values
from services.ocpp.security_event_notification import process_security_event_notification
from services.ocpp.start_transaction import process_start_transaction
from services.ocpp.status_notification import process_status_notification
from services.ocpp.stop_transaction import process_stop_transaction
from views.charge_points import ChargePointUpdateStatusView


@prepare_event
async def process_event(event):
    logger.info(f"Got event from charge point node (event={event})")

    async with get_contextual_session() as session:

        if event.action is Action.MeterValues:
            await process_meter_values(session, deepcopy(event))
        if event.action is Action.StopTransaction:
            await process_stop_transaction(session, deepcopy(event))
        if event.action is Action.StartTransaction:
            await process_start_transaction(session, deepcopy(event))
        if event.action is Action.Authorize:
            await process_authorize(session, deepcopy(event))
        if event.action is Action.SecurityEventNotification:
            await process_security_event_notification(session, deepcopy(event))
        if event.action is Action.BootNotification:
            await process_boot_notification(session, deepcopy(event))
            await init_configuration(charge_point_id=event.charge_point_id)
        if event.action is Action.StatusNotification:
            await process_status_notification(session, deepcopy(event))
        if event.action is Action.Heartbeat:
            await process_heartbeat(session, deepcopy(event))

        if event.action is ConnectionAction.lost_connection:
            data = ChargePointUpdateStatusView(status=ChargePointStatus.unavailable)
            await update_charge_point(session, charge_point_id=event.charge_point_id, data=data)
            await reset_connectors(session, event.charge_point_id)

        await session.commit()
        logger.info(f"Successfully completed process event={event}")

        return event
