import asyncio

import arrow
from ocpp.routing import on, after
from ocpp.v16 import call, call_result, ChargePoint as cp
from ocpp.v16.call import ChangeConfigurationPayload
from ocpp.v16.call_result import (
    BootNotificationPayload,
    StatusNotificationPayload,
    HeartbeatPayload, StartTransactionPayload
)
from ocpp.v16.datatypes import SampledValue, MeterValue, ChargingProfile
from ocpp.v16.enums import (
    Action,
    ConfigurationStatus,
    ChargePointErrorCode,
    ChargePointStatus,
    ResetType,
    ResetStatus,
    UnlockStatus, RemoteStartStopStatus, ReadingContext, Measurand, UnitOfMeasure, ValueFormat, Location,
    ChargingProfilePurposeType, ChargingProfileKindType
)

from core import settings
from core.database import get_contextual_session
from core.fields import TransactionStatus
from services.actions import get_all_actions
from services.charge_points import get_charge_point_or_404, get_connector_or_404
from services.ocpp.change_configuration import configuration
from services.transactions import get_transaction_or_404
from views.actions import ActionView

meter_value_power_active_import = SampledValue(
    value='0',
    context=ReadingContext.sample_periodic,
    format=ValueFormat.raw,
    measurand=Measurand.energy_active_import_register,
    location=Location.outlet,
    unit=UnitOfMeasure.w
)


class ChargePoint(cp):
    @on(Action.ChangeConfiguration, skip_schema_validation=True)
    async def change_configuration(self, key, value):
        conf = ChangeConfigurationPayload(key=key, value=value)
        assert conf in configuration, "Got invalid configuration from the server."
        return call_result.ChangeConfigurationPayload(status=ConfigurationStatus.accepted)

    @on(Action.RemoteStartTransaction)
    async def remote_start_transaction(
            self,
            connector_id: int,
            id_tag: str,
            charging_profile: ChargingProfile
    ):
        assert ChargingProfilePurposeType(
            ChargingProfile.charging_profile_purpose) is ChargingProfilePurposeType.tx_profile
        assert ChargingProfileKindType(ChargingProfile.charging_profile_kind) is ChargingProfileKindType.relative
        assert connector_id == 1
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Start transaction" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.pending
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")
            return call_result.RemoteStartTransactionPayload(status=RemoteStartStopStatus.accepted)

    @on(Action.RemoteStopTransaction)
    async def remote_stop_transaction(self, transaction_id):
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Stop transaction" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.pending
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")
            return call_result.RemoteStopTransactionPayload(status=RemoteStartStopStatus.accepted)

    @after(Action.RemoteStartTransaction)
    async def after_remote_start_transaction(self, connector_id, id_tag, charging_profile: ChargingProfile):
        await asyncio.sleep(1)
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Start transaction" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.completed, action_view.status
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")
            await asyncio.sleep(0.5)
            connector = await get_connector_or_404(session, charge_point.id, connector_id)
            assert ChargePointStatus(connector.status) is not ChargePointStatus.available, connector.status

    @on(Action.UnlockConnector)
    async def unlock_connector(self, connector_id):
        assert connector_id == 1
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Unlock" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.pending
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")
            return call_result.UnlockConnectorPayload(status=UnlockStatus.unlocked)

    @after(Action.UnlockConnector)
    async def after_unlock_connector(self, connector_id):
        await asyncio.sleep(0.5)
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Unlock" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.completed, action_view.status
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")

    @on(Action.Reset)
    async def reset(self, type):
        assert ResetType(type) is ResetType.soft
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Reset station" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.pending
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")
            return call_result.ResetPayload(status=ResetStatus.accepted)

    @after(Action.Reset)
    async def after_reset(self, type):
        await asyncio.sleep(0.5)
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            actions = await get_all_actions(charge_point.garage.id)
            for action in actions:
                action_view = ActionView(**action)
                if "Start transaction" in action_view.body:
                    assert TransactionStatus(action_view.status) is TransactionStatus.completed
                    assert action_view.charge_point_id == self.id
                    break
            else:
                raise Exception("Could not find action.")

    async def send_meter_values(self, transaction_id):
        step = 100
        for i in range(5):
            await asyncio.sleep(1)
            value = str(int(meter_value_power_active_import.value) + step)
            meter_value_power_active_import.value = value
            request = call.MeterValuesPayload(
                transaction_id=transaction_id,
                connector_id=1,
                meter_value=[
                    MeterValue(
                        timestamp=arrow.utcnow().isoformat(),
                        sampled_value=[meter_value_power_active_import]
                    )
                ]
            )
            await self.call(request)
            await asyncio.sleep(1)
            async with get_contextual_session() as session:
                transaction = await get_transaction_or_404(session, transaction_id)
                assert transaction.meter_stop == int(value)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="test",
            charge_point_vendor="ABB"
        )

        response: BootNotificationPayload = await self.call(request)
        assert response.interval == settings.HEARTBEAT_INTERVAL, "Got invalid heartbeat interval."
        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, self.id)
            assert charge_point.model == request.charge_point_model
            assert charge_point.vendor == request.charge_point_vendor

    async def send_status_notification(
            self,
            error_code=ChargePointErrorCode.no_error,
            status=ChargePointStatus.available
    ):
        for connector_id in [0, 1]:
            request = call.StatusNotificationPayload(
                connector_id=connector_id,
                error_code=error_code,
                status=status
            )
            response = await self.call(request)
            await asyncio.sleep(3)
            assert isinstance(response, StatusNotificationPayload)
            async with get_contextual_session() as session:
                charge_point = await get_charge_point_or_404(session, self.id)
                if connector_id == 0:
                    assert ChargePointStatus(charge_point.status) is status, "Invalid status"
                if connector_id > 0:
                    connector = await get_connector_or_404(session, self.id, connector_id)
                    assert ChargePointStatus(connector.status) is status, "Invalid status"

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
        response = await self.call(request)
        assert isinstance(response, HeartbeatPayload)

    async def start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag='some id tag',
            meter_start=0,  # Initial Energy meter value / integer
            timestamp=arrow.utcnow().isoformat()
        )
        response: StartTransactionPayload = await self.call(request)

        assert response.id_tag_info["status"] == "Accepted"
        await asyncio.sleep(0.5)
        async with get_contextual_session() as session:
            connector = await get_connector_or_404(session, self.id, request.connector_id)
            assert ChargePointStatus(connector.status) is ChargePointStatus.charging, connector.status
            transaction = await get_transaction_or_404(session, response.transaction_id)
            assert transaction.id == response.transaction_id
            assert transaction.charge_point == self.id
            assert transaction.meter_start == 0
            assert TransactionStatus(transaction.status) is TransactionStatus.in_progress
            return response.transaction_id

    async def stop_transaction(self, transaction_id):
        request = call.StopTransactionPayload(
            transaction_id=transaction_id,
            meter_stop=1000,
            timestamp=arrow.utcnow().isoformat()
        )
        response = await self.call(request)
        assert response.id_tag_info["status"] == "Accepted"
        await asyncio.sleep(1)
        async with get_contextual_session() as session:
            transaction = await get_transaction_or_404(session, transaction_id)
            assert transaction.meter_stop == request.meter_stop
            assert TransactionStatus(transaction.status) is TransactionStatus.completed
