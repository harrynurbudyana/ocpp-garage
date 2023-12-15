from fastapi import Depends
from ocpp.v16.enums import ChargePointStatus
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from exceptions import Forbidden
from services.charge_points import get_connector_or_404
from views.payments import PaymentContext


async def use_data_if_allowed(data: PaymentContext, session: AsyncSession = Depends(get_session)):
    connector = await get_connector_or_404(session, data.charge_point_id, data.connector_id)
    if ChargePointStatus(connector.status) is not ChargePointStatus.available:
        raise Forbidden(detail="Connector is already taken.")
    return data
