from sqlalchemy import delete

from core.database import get_contextual_session
from models import Transaction
from services.charge_points import create_charge_point, remove_charge_point
from services.garages import list_simple_garages
from views.charge_points import CreateChargPointView

TEST_CHARGE_POINT_NAME = "test_charge_point"


async def init_test_station(charge_point_id):
    async with get_contextual_session() as session:
        garages = await list_simple_garages(session)
        garage = garages[0]
        data = CreateChargPointView(id=charge_point_id)
        await create_charge_point(session, garage.id, data)
        await session.commit()


async def drop_test_station_with_transactions(charge_point_id):
    async with get_contextual_session() as session:
        await remove_charge_point(session, charge_point_id)
        query = delete(Transaction).where(Transaction.charge_point == charge_point_id)
        await session.execute(query)
        await session.commit()
