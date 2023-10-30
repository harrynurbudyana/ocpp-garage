from __future__ import annotations

import os

from loguru import logger

DEBUG = os.environ.get("DEBUG") == "1"

DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

REDIS_HOST = os.environ["REDIS_HOST"]

DATABASE_ASYNC_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_SYNC_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

logger.add(
    "csms.log",
    enqueue=True,
    backtrace=True,
    diagnose=DEBUG,
    format="{time} - {level} - {message}",
    rotation="500 MB",
    level="INFO"
)

DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss"
UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

ALLOWED_ORIGIN = os.environ["ALLOWED_ORIGIN"]

EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"] == '1'
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_FROM = os.environ["EMAIL_FROM"]

NORDPOOL_PRICES_URL = "https://www.nordpoolgroup.com/api/marketdata/page/23?currency=NOK&endDate={}"  # date format "28-10-2023"
NORDPOLL_PRICES_REQUSTED_DATE_FORMAT = "%d-%m-%Y"

NORDPOOL_REGION = os.environ["NORDPOOL_REGION"]
assert NORDPOOL_REGION in [f"NO{i}" for i in range(1, 6)]

DAILY_HOURS_RANGE = range(6, 22)
STATIC_PATH = "/tmp/static"

HTTP_TIMEOUT = 10
