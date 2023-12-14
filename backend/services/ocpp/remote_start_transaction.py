import random
from dataclasses import asdict

from loguru import logger
from ocpp.v16.call import RemoteStartTransactionPayload
from ocpp.v16.datatypes import ChargingProfile, ChargingSchedule, ChargingSchedulePeriod
from ocpp.v16.enums import ChargePointStatus, Action, RemoteStartStopStatus, ChargingProfilePurposeType, \
    ChargingProfileKindType, ChargingRateUnitType
from pyocpp_contrib.decorators import send_call, contextable, use_context
from pyocpp_contrib.v16.views.events import RemoteStartTransactionCallResultEvent
from sqlalchemy.ext.asyncio import AsyncSession

from core.fields import TransactionStatus
from services.actions import extend_actions_list, update_actions_status
from services.charge_points import get_charge_point_or_404, update_connector
from views.actions import ActionView
from views.charge_points import UpdateChargPointView


@contextable
@send_call(Action.RemoteStartTransaction)
async def process_remote_start_transaction_call(
        session: AsyncSession,
        limit: int,
        charge_point_id: str,
        connector_id: int,
        id_tag: str,
        message_id: str
) -> RemoteStartTransactionPayload:
    charge_point = await get_charge_point_or_404(session, charge_point_id)
    logger.info(
        f"RemoteStartTransaction -> | Found charge point (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")

    # Declare charging profile per transaction.
    # https://docs.edrv.io/docs/set-charging-profiles
    charging_profile = ChargingProfile(
        charging_profile_id=random.choice(range(1000)),  # Unique identifier for this profile.
        stack_level=1,  # Value determining level in hierarchy stack of profiles.

        # Profile with constraints to be imposed by the Charge Point on the current transaction.
        charging_profile_purpose=ChargingProfilePurposeType.tx_profile,

        # Schedule periods are relative to a situation- specific start point
        # (such as the start of a session) that is determined by the charge point.
        charging_profile_kind=ChargingProfileKindType.relative,

        charging_schedule=ChargingSchedule(
            charging_rate_unit=ChargingRateUnitType.watts,
            charging_schedule_period=[
                ChargingSchedulePeriod(
                    start_period=0,  # Start of the period, in seconds from the start of schedule.
                    limit=float(limit)
                )
            ]
        )
    )

    data = UpdateChargPointView(
        status=ChargePointStatus.preparing,
        latest_limit=limit
    )
    await update_connector(session, charge_point_id, connector_id, data)
    logger.info(
        f"RemoteStartTransaction -> | Updated connector with data={data} (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")
    payload = RemoteStartTransactionPayload(
        connector_id=connector_id,
        id_tag=id_tag,
        charging_profile=asdict(charging_profile)
    )
    logger.info(
        f"RemoteStartTransaction -> | Prepared payload={payload} (charge_point_id={charge_point_id}, connector_id={connector_id}, id_tag={id_tag})")

    action = ActionView(
        message_id=message_id,
        charge_point_id=charge_point_id,
        connector_id=connector_id,
        body=f"Start transaction"
    )
    await extend_actions_list(charge_point.garage_id, action)

    return payload


@use_context
async def process_remote_start_transaction_call_result(
        session: AsyncSession,
        event: RemoteStartTransactionCallResultEvent,
        context: RemoteStartTransactionPayload | None = None
):
    logger.info(f"<- RemoteStartTransaction | Start process call result response (event={event}, context={context}.)")
    charge_point = await get_charge_point_or_404(session, event.charge_point_id)

    if RemoteStartStopStatus(event.payload.status) is RemoteStartStopStatus.accepted:
        await update_actions_status(charge_point.garage_id, event.message_id, status=TransactionStatus.completed)
    else:
        await update_actions_status(charge_point.garage_id, event.message_id, status=TransactionStatus.faulted)
        data = UpdateChargPointView(status=ChargePointStatus.available)
        await update_connector(session, event.charge_point_id, context.connector_id, data)
