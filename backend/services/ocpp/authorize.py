from dataclasses import asdict

from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16.enums import AuthorizationStatus
from pyocpp_contrib.v16.views.events import AuthorizeEvent
from pyocpp_contrib.v16.views.tasks import AuthorizeResponse

from services.charge_points import get_charge_point


async def process_authorize(session, event: AuthorizeEvent) -> AuthorizeResponse:
    status = AuthorizationStatus.accepted
    charge_point = await get_charge_point(session, event.charge_point_id)
    if not charge_point.driver or not charge_point.driver.is_active:
        status = AuthorizationStatus.blocked
    return AuthorizeResponse(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        id_tag_info=asdict(IdTagInfo(status=status))
    )
