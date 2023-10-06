from dataclasses import asdict

from ocpp.v16.call_result import AuthorizePayload
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import AuthorizationStatus
from pyocpp_contrib.v16.views.events import AuthorizeCallEvent
from pyocpp_contrib.v16.views.tasks import AuthorizeCallResultTask

from services.charge_points import get_charge_point
from services.drivers import is_driver_authorized


async def process_authorize(session, event: AuthorizeCallEvent) -> AuthorizeCallResultTask:
    status = AuthorizationStatus.accepted
    charge_point = await get_charge_point(session, event.charge_point_id)
    if not charge_point.driver or not await is_driver_authorized(charge_point.driver):
        status = AuthorizationStatus.blocked

    payload = AuthorizePayload(id_tag_info=asdict(IdTagInfo(status=status)))
    return AuthorizeCallResultTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        payload=payload
    )
