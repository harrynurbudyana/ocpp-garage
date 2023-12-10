from typing import List

from passlib.context import CryptContext
from pyocpp_contrib.cache import get_connection
from sqlalchemy import select, or_, func, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import selectable
from starlette.background import BackgroundTasks

from core import settings
from core.database import generate_default_id
from core.fields import NotificationType
from exceptions import NotFound
from models import User
from views.users import CreateUserView
from views.users import InviteUserView

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def build_users_query(
        search: str,
        extra_criterias: List | None = None
) -> selectable:
    query = select(User)
    if extra_criterias:
        for criteria in extra_criterias:
            query = query.where(criteria)
    query = query.order_by(User.updated_at.asc())
    if search:
        query = query.where(or_(
            func.lower(User.email).contains(func.lower(search)),
            func.cast(User.address, String).ilike(f"{search}%"),
            func.lower(User.first_name).contains(func.lower(search)),
            func.lower(User.last_name).contains(func.lower(search)),
        ))
    return query


async def get_user_or_404(session: AsyncSession, value: str) -> User:
    result = await session.execute(
        select(User) \
            .where(or_(User.id == value, User.email == value))
    )
    user = result.scalars().first()
    if not user:
        raise NotFound(detail="The user is not found.")
    return user


async def invite_user(
        garage_id: str,
        data: InviteUserView,
        background_tasks: BackgroundTasks
):
    from services.notifications import send_notification

    data.garage_id = garage_id
    data.id = generate_default_id()

    connection = await get_connection()
    await connection.set(data.id, data.json())
    await connection.expire(data.id, settings.INVITATION_LINK_EXPIRE_AFTER)

    link = settings.ALLOWED_ORIGIN + f"/signup/{data.id}"

    background_tasks.add_task(
        send_notification,
        data.email,
        NotificationType.new_user_invited,
        dict(link=link)
    )


async def create_user(
        session: AsyncSession,
        data: CreateUserView,
        garage_id: str | None = None
) -> User:
    data.password = pwd_context.hash(data.password)
    user = User(**data.dict(exclude_none=True))
    user.garage_id = garage_id
    session.add(user)
    return user
