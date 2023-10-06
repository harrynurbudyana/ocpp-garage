from ocpp.v16.call import ResetPayload
from ocpp.v16.enums import ResetType
from pyocpp_contrib.v16.views.tasks import ResetCallTask


async def process_reset(charge_point_id: str) -> ResetCallTask:
    payload = ResetPayload(type=ResetType.soft)
    return ResetCallTask(
        charge_point_id=charge_point_id,
        payload=payload
    )
