import json
from typing import List, Dict

from core.cache import get_connection
from core.settings import MAX_ACTIONS_LENGTH
from views.actions import ActionView


async def extend_actions_list(garage_id: str, value: ActionView):
    garage_id = str(garage_id)
    conn = await get_connection()
    await conn.lpush(garage_id, value.json())
    await conn.ltrim(garage_id, 0, MAX_ACTIONS_LENGTH)


async def get_all_actions(garage_id: str) -> List[Dict]:
    conn = await get_connection()
    stored_data = await conn.lrange(str(garage_id), 0, -1)
    return [json.loads(item) for item in stored_data]


async def update_actions_status(garage_id, message_id, status):
    conn = await get_connection()
    garage_id = str(garage_id)
    actions = await get_all_actions(garage_id)
    for idx, item in enumerate(actions):
        action = ActionView(**item)
        if action.message_id == message_id:
            action.status = status
            await conn.lset(garage_id, idx, action.json())
