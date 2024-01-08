from ocpp.v16.call import ChangeConfigurationPayload
from ocpp.v16.enums import Action
from ocpp.v16.enums import ConfigurationKey, Measurand

from pyocpp_contrib.decorators import send_call

configuration = [
    ChangeConfigurationPayload(
        # The charge point will immediately start a transaction for the idTag given in the RemoteStartTransaction.req message
        key=ConfigurationKey.authorize_remote_tx_requests,
        # the Charge Point will not first try to authorize the idTag
        value=False
    ),
    # ChangeConfigurationPayload(
    #     key=ConfigurationKey.unlock_connector_on_ev_side_disconnect,
    #     # unlock connector once transaction stopped
    #     value=True
    # ),
    # ChangeConfigurationPayload(
    #     key=ConfigurationKey.stop_transaction_on_ev_side_disconnect,
    #     # transaction will be stopped once connector disconnected
    #     # will prevent sabotage acts top stop the energy flow by unplugging not locked cables on EV side.
    #     value=True
    # ),
    ChangeConfigurationPayload(
        key=ConfigurationKey.meter_value_sample_interval,
        value=60  # one minute
    ),
    ChangeConfigurationPayload(
        key=ConfigurationKey.meter_values_sampled_data,
        # Energy imported by EV (Wh or kWh)
        value=Measurand.energy_active_import_register
    ),
    ChangeConfigurationPayload(
        # Interval (from successful authorization) until incipient charging session
        # is automatically canceled due to failure of EV user to (correctly)
        # insert the charging cable connector(s) into the appropriate connector(s).
        key=ConfigurationKey.connection_time_out,
        value=300  # 5 minutes
    )
]


@send_call(Action.ChangeConfiguration)
async def process_change_configration_call(
        config: ChangeConfigurationPayload,
        charge_point_id: str,
        message_id: str
) -> ChangeConfigurationPayload:
    return config
