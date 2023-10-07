from ocpp.v16.call import ResetPayload
from ocpp.v16.enums import ResetType, Action
from pyocpp_contrib.decorators import send_call


@send_call(Action.Reset)
async def process_reset(charge_point_id: str) -> ResetPayload:
    return ResetPayload(type=ResetType.soft)
