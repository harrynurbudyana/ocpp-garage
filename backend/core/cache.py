import json
from typing import Dict, List

import redis.asyncio as redis

from core import settings
from views.actions import ActionView


class Cache:
    def __init__(self, host=settings.REDIS_HOST):
        self.conn = redis.from_url(f"redis://{host}")

    async def set(self, key, value, expire=None):
        await self.conn.set(key, json.dumps(value))
        if expire:
            await self.conn.expire(key, expire)

    async def get(self, key):
        context: bytes | None = await self.conn.get(key)
        try:
            return json.loads(context.decode())
        except AttributeError:
            return context


class ActionCache(Cache):
    max_actions_length = 30

    async def get_all_actions(self, garage_id: str) -> List[Dict]:
        stored_data = await self.conn.lrange(str(garage_id), 0, -1)
        return [json.loads(item) for item in stored_data]

    async def insert(self, garage_id: str, value: ActionView):
        garage_id = str(garage_id)
        await self.conn.lpush(garage_id, value.json())
        await self.conn.ltrim(garage_id, 0, self.max_actions_length)

    async def update_status(self, garage_id, message_id, status):
        garage_id = str(garage_id)
        actions = await self.get_all_actions(garage_id)
        for idx, item in enumerate(actions):
            action = ActionView(**item)
            if action.message_id == message_id:
                action.status = status
                await self.conn.lset(garage_id, idx, action.json())
