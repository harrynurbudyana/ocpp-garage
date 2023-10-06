from typing import List

from ocpp.v16.call import ChangeConfigurationPayload
from ocpp.v16.enums import ConfigurationKey
from pyocpp_contrib.v16.views.tasks import ChangeConfigurationCallTask


async def init_configuration(charge_point_id: str) -> List[ChangeConfigurationCallTask]:
    tasks = [
        ChangeConfigurationPayload(
            # The charge point will immediately start a transaction for the idTag given in the RemoteStartTransaction.req message
            key=ConfigurationKey.authorize_remote_tx_requests,
            # the Charge Point will not first try to authorize the idTag
            value=False
        ),
        ChangeConfigurationPayload(
            key=ConfigurationKey.unlock_connector_on_ev_side_disconnect,
            # unlock connector once transaction stopped
            value=True
        ),
        ChangeConfigurationPayload(
            key=ConfigurationKey.stop_transaction_on_ev_side_disconnect,
            # transaction will be stopped once connector disconnected
            # will prevent sabotage acts top stop the energy flow by unplugging not locked cables on EV side.
            value=True
        )
    ]
    return [
        ChangeConfigurationCallTask(
            charge_point_id=charge_point_id,
            payload=payload
        ) for payload in tasks]
