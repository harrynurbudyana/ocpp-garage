from sqlalchemy import select, func, or_

from models import GridProvider


async def retrieve_grid_providers(session, search: str):
    criterias = [
        GridProvider.is_active.is_(True)
    ]
    query = select(GridProvider)
    for criteria in criterias:
        query = query.where(criteria)

    if search:
        query = query.where(or_(
            func.lower(GridProvider.name).contains(func.lower(search)),
            func.lower(GridProvider.postnummer).contains(func.lower(search))
        ))
    query = query.order_by(GridProvider.postnummer.asc())
    result = await session.execute(
        query.with_only_columns(
            GridProvider.id,
            GridProvider.name,
            GridProvider.postnummer
        )
    )
    return result.unique().fetchall()
