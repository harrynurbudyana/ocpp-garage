from datetime import timedelta, datetime
from typing import List


def generate_hour_ranges_with_rates(start: datetime, end: datetime) -> List:
    """
    Accepts:
        - datetime(2023-10-15T15:32:87)
        - datetime(2023-10-15T02:19:19)
    Returns a list:
    [
        ("15:32", "16:00"),
        ("16:00", "17:00"),
        ("17:00", "18:00"),
        ("18:00", "19:00"),
        ("19:00", "20:00"),
        ("20:00", "21:00"),
        ("21:00", "22:00"),
        ("22:00", "23:00"),
        ("23:00", "0:00"),
        ("00:00", "1:00"),
        ("1:00", "2:00"),
        ("2:00", "2:19")
    ]
    """
    hour_ranges = []

    daily_range = range(6, 22)
    daily_rate = 0.45
    nightly_rate = 0.29

    if start.hour in daily_range:
        rate = daily_rate
    else:
        rate = nightly_rate
    hour_ranges.append((f"{start.hour}:{start.minute}", f"{start.hour + 1}:00", rate))
    next_hour = start + timedelta(hours=1)
    start = next_hour

    while start < end:
        next_hour = start + timedelta(hours=1)
        if start.hour in daily_range:
            rate = daily_rate
        else:
            rate = nightly_rate
        hour_ranges.append((f"{start.hour}:00", f"{next_hour.hour}:00", rate))
        start = next_hour

    if end.hour in daily_range:
        rate = daily_rate
    else:
        rate = nightly_rate
    hour_ranges[-1] = hour_ranges[-1][0], f"{end.hour}:{end.minute}", rate

    return hour_ranges
