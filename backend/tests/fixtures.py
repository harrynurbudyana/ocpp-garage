from faker import Faker
from faker.exceptions import UniquenessException
from sqlalchemy import text

from core.database import get_contextual_session
from services.charge_points import create_charge_point
from views.charge_points import CreateChargPointView


async def create_dummy_charge_points(count):
    Faker.seed(0)
    fake = Faker()
    data = {
        "id": lambda: fake.unique.bothify(text='????########', letters='ABCDE'),
        "description": lambda: fake.sentence(nb_words=5),
        "manufacturer": lambda: fake.company(),
        "serial_number": lambda: fake.unique.bothify(text='????###########', letters='QWER'),
        "model": lambda: fake.unique.pyint(),
        "location": lambda: "parking space %d" % fake.pyint(min_value=1, max_value=count * 2, step=1),
    }
    async with get_contextual_session() as session:
        for i in range(count):
            try:
                view = CreateChargPointView(**{k: v() for k, v in data.items()})
            except UniquenessException:
                continue
            await create_charge_point(session, view)
            await session.commit()

    async with get_contextual_session() as session:
        await session.execute(text(
            """UPDATE charge_points SET connectors = '{"1": {"status": "unavailable"}, "2": {"status": "unavailable"}}';"""))
        await session.commit()


async def create_dummy_data(
        charge_points=53,
):
    await create_dummy_charge_points(charge_points)
