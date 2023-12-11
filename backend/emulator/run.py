import asyncio

import websockets
from pyocpp_contrib.decorators import message_id_generator

from core.database import get_contextual_session
from core.settings import WS_SERVER_PORT
from emulator import TEST_CHARGE_POINT_NAME, init_test_station, drop_test_station_with_transactions
from emulator.charge_point import ChargePoint
from services.ocpp.remote_start_transaction import process_remote_start_transaction_call
from services.ocpp.reset import process_reset
from services.ocpp.unlock_connector import process_unlock_connector


async def run_tests(charge_point_id):
    tasks = []
    async with websockets.connect(
            f'ws://ocpp-gateway:{WS_SERVER_PORT}/{charge_point_id}',
            subprotocols=['ocpp1.6']
    ) as ws:
        cp = ChargePoint(charge_point_id, ws)

        task = asyncio.create_task(cp.start())
        tasks.append(task)

        print(" --- Start send boot notification.")
        await asyncio.sleep(2)
        await cp.send_boot_notification()
        print(" --- Start send status notifications.")
        await asyncio.sleep(2)
        await cp.send_status_notification()
        print(" --- Start send heartbeat.")
        await asyncio.sleep(2)
        await cp.send_heartbeat()
        print(" --- Start request reset.")
        await asyncio.sleep(3)
        async with get_contextual_session() as session:
            await process_reset(
                session,
                charge_point_id=charge_point_id,
                message_id=message_id_generator()
            )
        print(" --- Start request unlock connector.")
        await asyncio.sleep(3)
        async with get_contextual_session() as session:
            await process_unlock_connector(
                session,
                charge_point_id=charge_point_id,
                connector_id=1,
                message_id=message_id_generator()
            )
        print("  --- Start remote transaction.")
        await asyncio.sleep(3)
        async with get_contextual_session() as session:
            await process_remote_start_transaction_call(
                session,
                charge_point_id=charge_point_id,
                connector_id=1,
                id_tag="some id tag",
                message_id=message_id_generator()
            )
            await session.commit()
        print(" --- Start new transaction.")
        await cp.start_transaction()

        await asyncio.sleep(5)
        print(" --- Completed.")


async def main():
    await init_test_station(TEST_CHARGE_POINT_NAME)
    await asyncio.sleep(3)

    await run_tests(TEST_CHARGE_POINT_NAME)

    await asyncio.sleep(3)
    await drop_test_station_with_transactions(TEST_CHARGE_POINT_NAME)


if __name__ == '__main__':
    asyncio.run(main())
