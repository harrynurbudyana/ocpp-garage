from copy import deepcopy
from functools import wraps
from typing import Callable, Union

from loguru import logger
from ocpp.v16.enums import Action, ChargePointStatus
from pyocpp_contrib.enums import ConnectionAction
from pyocpp_contrib.queue.publisher import publish
from pyocpp_contrib.v16.views.events import (
    LostConnectionEvent,
    SecurityEventNotificationCallEvent,
    StatusNotificationCallEvent,
    BootNotificationCallEvent,
    HeartbeatCallEvent,
    AuthorizeCallEvent,
    StartTransactionCallEvent,
    StopTransactionCallEvent,
    MeterValuesCallEvent,
    ClearCacheCallResultEvent,
    ChangeConfigurationCallResultEvent,
    ChangeAvailabilityCallResultEvent,
    DataTransferCallResultEvent,
    GetConfigurationCallResultEvent,
    RemoteStartTransactionCallResultEvent,
    RemoteStopTransactionCallResultEvent,
    ResetCallResultEvent,
    UnlockConnectorCallResultEvent
)

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


def prepare_event(func) -> Callable:
    @wraps(func)
    async def wrapper(data):
        logger.info(f"Got event from charge point node (event={data})")

        event = {
            ConnectionAction.lost_connection: LostConnectionEvent,
            Action.StatusNotification: StatusNotificationCallEvent,
            Action.BootNotification: BootNotificationCallEvent,
            Action.Heartbeat: HeartbeatCallEvent,
            Action.SecurityEventNotification: SecurityEventNotificationCallEvent,
            Action.Authorize: AuthorizeCallEvent,
            Action.StartTransaction: StartTransactionCallEvent,
            Action.StopTransaction: StopTransactionCallEvent,
            Action.MeterValues: MeterValuesCallEvent,
            Action.ClearCache: ClearCacheCallResultEvent,
            Action.ChangeConfiguration: ChangeConfigurationCallResultEvent,
            Action.ChangeAvailability: ChangeAvailabilityCallResultEvent,
            Action.DataTransfer: DataTransferCallResultEvent,
            Action.GetConfiguration: GetConfigurationCallResultEvent,
            Action.RemoteStartTransaction: RemoteStartTransactionCallResultEvent,
            Action.RemoteStopTransaction: RemoteStopTransactionCallResultEvent,
            Action.Reset: ResetCallResultEvent,
            Action.UnlockConnector: UnlockConnectorCallResultEvent
        }[data["action"]](**data)
        return await func(event)

    return wrapper


@prepare_event
async def process_event(event: Union[
    LostConnectionEvent,
    StatusNotificationCallEvent,
    BootNotificationCallEvent,
    HeartbeatCallEvent,
    SecurityEventNotificationCallEvent,
    AuthorizeCallEvent,
    StartTransactionCallEvent,
    StopTransactionCallEvent,
    MeterValuesCallEvent,
    ClearCacheCallResultEvent,
    ChangeConfigurationCallResultEvent,
    ChangeAvailabilityCallResultEvent,
    DataTransferCallResultEvent,
    GetConfigurationCallResultEvent,
    RemoteStartTransactionCallResultEvent,
    RemoteStopTransactionCallResultEvent,
    ResetCallResultEvent,
    UnlockConnectorCallResultEvent
]):
    task = None

    async with get_contextual_session() as session:

        if event.action is Action.MeterValues:
            task = await process_meter_values(session, deepcopy(event))
        if event.action is Action.StopTransaction:
            task = await process_stop_transaction(session, deepcopy(event))
        if event.action is Action.StartTransaction:
            task = await process_start_transaction(session, deepcopy(event))
        if event.action is Action.Authorize:
            task = await process_authorize(session, deepcopy(event))
        if event.action is Action.SecurityEventNotification:
            task = await process_security_event_notification(session, deepcopy(event))
        if event.action is Action.BootNotification:
            task = await process_boot_notification(session, deepcopy(event))
        if event.action is Action.StatusNotification:
            task = await process_status_notification(session, deepcopy(event))
        if event.action is Action.Heartbeat:
            task = await process_heartbeat(session, deepcopy(event))

        if event.action is ConnectionAction.lost_connection:
            data = ChargePointUpdateStatusView(status=ChargePointStatus.unavailable)
            await update_charge_point(session, charge_point_id=event.charge_point_id, data=data)
            await reset_connectors(session, event.charge_point_id)

        if task:
            await publish(task.json(), to=task.exchange, priority=task.priority)

        if event.action is Action.BootNotification:
            task = await init_configuration(event.charge_point_id)
            await publish(task.json(), to=task.exchange, priority=task.priority)

        await session.commit()
        logger.info(f"Successfully completed process event={event}")

        return event
