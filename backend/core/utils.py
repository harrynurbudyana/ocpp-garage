from __future__ import annotations

import arrow

from core.settings import UTC_DATETIME_FORMAT


def get_utc_as_string() -> str:
    return arrow.utcnow().datetime.strftime(UTC_DATETIME_FORMAT)


def now():
    return arrow.utcnow()


def make_key_for_cache(charge_point_id: str, connector_id: int) -> str:
    return f"{charge_point_id}_{connector_id}"
