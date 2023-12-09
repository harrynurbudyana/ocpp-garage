from ocpp.v16.call_result import AuthorizePayload
from ocpp.v16.enums import Action
from sqlalchemy.ext.asyncio import AsyncSession

from pyocpp_contrib.decorators import response_call_result
from pyocpp_contrib.v16.views.events import AuthorizeCallEvent

@response_call_result(Action.Authorize)
async def process_authorize(
        session: AsyncSession,
        event: AuthorizeCallEvent
) -> AuthorizePayload:
    pass
