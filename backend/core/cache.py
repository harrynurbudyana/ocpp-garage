import redis.asyncio as redis

from core import settings

_conn = None


async def get_connection(host=settings.REDIS_HOST):
    global _conn
    if not _conn:
        _conn = redis.from_url(f"redis://{host}")
    return _conn




