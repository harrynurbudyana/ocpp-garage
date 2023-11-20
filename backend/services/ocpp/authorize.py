from ocpp.v16.call_result import AuthorizePayload
from ocpp.v16.enums import Action

from pyocpp_contrib.decorators import response_call_result


@response_call_result(Action.Authorize)
async def process_authorize(session, event) -> AuthorizePayload:
    pass
