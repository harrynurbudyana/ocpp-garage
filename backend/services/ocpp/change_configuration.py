from uuid import uuid4

from ocpp.v16.call import ChangeConfigurationPayload
from ocpp.v16.enums import ConfigurationKey
from pyocpp_contrib.v16.views.tasks import ChangeConfigurationCallTask


async def init_configuration(charge_point_id: str) -> ChangeConfigurationCallTask:
    # The charge point will immediately start a transaction for the idTag given in the RemoteStartTransaction.req message
    payload = ChangeConfigurationPayload(
        key=ConfigurationKey.authorize_remote_tx_requests,
        # the Charge Point will not first try to authorize the idTag
        value=False
    )
    return ChangeConfigurationCallTask(
        message_id=str(uuid4()),
        charge_point_id=charge_point_id,
        payload=payload
    )
