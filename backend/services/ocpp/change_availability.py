from ocpp.v16.call import ChangeAvailabilityPayload
from ocpp.v16.enums import AvailabilityType
from pyocpp_contrib.v16.views.tasks import ChangeAvailabilityCallTask


async def process_change_availability(
        charge_point_id: str,
        connector_id: int,
        type: AvailabilityType
) -> ChangeAvailabilityCallTask:
    payload = ChangeAvailabilityPayload(connector_id=connector_id, type=type)
    return ChangeAvailabilityCallTask(
        charge_point_id=charge_point_id,
        payload=payload
    )
