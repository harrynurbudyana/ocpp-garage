import argparse
import asyncio

from loguru import logger
from sqlalchemy.exc import IntegrityError, DBAPIError

from core.database import get_contextual_session
from services.operators import create_operator
from views.operators import CreateOperatorView


async def run(email, password):
    view = CreateOperatorView(email=email, password=password)
    async with get_contextual_session() as session:
        user = await create_operator(session, view)
        try:
            await session.commit()
        except IntegrityError:
            logger.warning("The user with given email already exists.")
            return
        except DBAPIError:
            import traceback
            logger.error("Too long values.")
            return

    logger.success(f"Successfully created user with email={user.email} and password={password}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--email", type=str, required=True)
    parser.add_argument("-p", "--password", type=str, required=True)
    args = parser.parse_args()

    asyncio.run(run(email=args.email, password=args.password))
