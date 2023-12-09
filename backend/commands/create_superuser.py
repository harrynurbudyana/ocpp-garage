import argparse
import asyncio

from loguru import logger
from sqlalchemy.exc import IntegrityError, DBAPIError

from core.database import get_contextual_session
from services.users import create_user
from views.users import CreateUserView


async def run(email, password, first_name):
    view = CreateUserView(
        email=email,
        first_name=first_name,
        password=password,
        is_superuser=True
    )
    async with get_contextual_session() as session:
        user = await create_user(session, view)
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
    parser.add_argument("-f", "--fname", type=str, required=True)
    args = parser.parse_args()

    asyncio.run(run(
        email=args.email,
        password=args.password,
        first_name=args.fname
    ))
