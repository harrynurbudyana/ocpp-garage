import calendar
from datetime import timedelta, datetime, time, date
from traceback import format_exc
from typing import List, Type

import arrow
import httpx
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from sqlalchemy import select

from core.settings import (
    NORDPOOL_REGION,
    NORDPOLL_PRICES_REQUSTED_DATE_FORMAT,
    NORDPOOL_PRICES_URL,
    DAILY_HOURS_RANGE
)
from models import Garage, Driver, Transaction, SpotPrice
from views.statements import TransactionsHourlyPeriod, StatementsTransaction, DriversStatement


async def persist_daily_nordpool_price(session, target_date: date, region=NORDPOOL_REGION):
    query = select(SpotPrice).where(SpotPrice.date == target_date)
    result = await session.execute(query)
    if result.scalars().first():
        logger.info(f"The price for given date already exists (date={target_date})")
        return

    hourly_prices = {}

    while not hourly_prices:
        try:
            url = NORDPOOL_PRICES_URL.format(target_date.strftime(NORDPOLL_PRICES_REQUSTED_DATE_FORMAT))
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                data = response.json()
        except Exception:
            logger.error("Could not obtain data from nordpool, error=%r" % format_exc())
            return
        else:
            for item in data["data"]["Rows"]:
                end_hour = arrow.get(item["EndTime"]).hour
                if any([arrow.get(item["StartTime"]).hour, end_hour]):
                    idx = int(region[-1]) - 1
                    value = item["Columns"][idx]["Value"].replace(",", ".")
                    hourly_prices[end_hour] = float(value)

        prices = [hourly_prices[key] for key in hourly_prices]
        spot_price = SpotPrice(date=target_date, hourly_prices=prices)
        logger.info(f"Successfully completed nordprices request (date={target_date}, hourly_prices={prices})")
        session.add(spot_price)


async def generate_hourly_ranges(
        start: datetime,
        end: datetime,
        view_class: Type[TransactionsHourlyPeriod] = TransactionsHourlyPeriod
) -> List[TransactionsHourlyPeriod]:
    """
    Accepts:
        - datetime(2023-10-15T15:32:87)
        - datetime(2023-10-15T02:19:19)
    Returns a list:
    [
        SingleDriverStatementPeriod(start=datetime.time(15,32), end=datetime.time(16, 0)),
        SingleDriverStatementPeriod(start=datetime.time(16, 0), end=datetime.time(17, 0)),
        SingleDriverStatementPeriod(start=datetime.time(17, 0), end=datetime.time(18, 0)),
        SingleDriverStatementPeriod(start=datetime.time(18, 0), end=datetime.time(19, 0)),
        SingleDriverStatementPeriod(start=datetime.time(19,0), end=datetime.time(20, 0)),
        SingleDriverStatementPeriod(start=datetime.time(20,0), end=datetime.time(21, 0)),
        SingleDriverStatementPeriod(start=datetime.time(21,0), end=datetime.time(22, 0)),
        SingleDriverStatementPeriod(start=datetime.time(22,0), end=datetime.time(23, 0)),
        SingleDriverStatementPeriod(start=datetime.time(23, 0), end=datetime.time(0, 0)),
        SingleDriverStatementPeriod(start=datetime.time(0,0), end=datetime.time(1, 0)),
        SingleDriverStatementPeriod(start=datetime.time(1,0), end=datetime.time(2, 0)),
        SingleDriverStatementPeriod(start=datetime.time(2,0), end=datetime.time(2, 19)),
    ]
    """
    hour_ranges = []

    next_hour = start + timedelta(hours=1)
    if next_hour > end:
        view = view_class(start=time(start.hour, start.minute, start.second),
                          end=time(end.hour, end.minute, end.second))
        hour_ranges.append(view)
        return hour_ranges

    view = view_class(start=time(start.hour, start.minute, start.second), end=time(start.hour + 1, 0, 0))
    hour_ranges.append(view)
    next_hour = start + timedelta(hours=1)
    start = next_hour

    while True:
        if start > end:
            view = view_class(start=time(end.hour, 0, 0), end=time(end.hour, end.minute, end.second))
            hour_ranges.append(view)
            break
        next_hour = start + timedelta(hours=1)
        view = view_class(start=time(start.hour, 0, 0), end=time(next_hour.hour, 0, 0))
        hour_ranges.append(view)
        start = next_hour

    return hour_ranges


async def detect_rates_for_periods(
        daily_rate: float,
        nightly_rate: float,
        views: List[TransactionsHourlyPeriod]
) -> List[TransactionsHourlyPeriod]:
    for view in views:
        if view.start.hour in DAILY_HOURS_RANGE:
            view.rate = daily_rate
        else:
            view.rate = nightly_rate
    if views[-1].end.hour in DAILY_HOURS_RANGE:
        views[-1].rate = daily_rate
    else:
        views[-1].rate = nightly_rate
    return views


async def get_transactions_hourly_explication(
        garage: Garage,
        transaction: Transaction
) -> List[TransactionsHourlyPeriod]:
    hourly_ranges = await generate_hourly_ranges(transaction.created_at, transaction.updated_at)
    hourly_ranges_with_rates = await detect_rates_for_periods(garage.daily_rate, garage.nightly_rate, hourly_ranges)
    return hourly_ranges_with_rates


async def generate_statements_for_driver(
        garage: Garage,
        driver: Driver,
        transactions: List[Transaction],
        month: int,
        year: int
):
    env = Environment(loader=FileSystemLoader('templates/statements'))
    total_kw = 0
    total_cost = 0
    statement_items = []
    for transaction in transactions:
        total_kw += (transaction.meter_stop - transaction.meter_start) / 1000
        transaction_view = StatementsTransaction(
            start=transaction.created_at,
            end=transaction.updated_at,
            nordpool_price=0,
            grid_cost=0,
            government_rebate=0,
            total_cost=0,
            per_kw_cost=0,
            hours=await get_transactions_hourly_explication(garage, transaction)
        )
        total_cost += transaction_view.total_cost
        statement_items.append(transaction_view)
    statement = DriversStatement(
        month=calendar.month_name[month],
        year=year,
        total_kw=total_kw,
        total_cost=total_cost,
        per_kw_cost=total_cost / total_kw if total_kw else 0,
        name=f"{driver.first_name} {driver.last_name}",
        email=driver.email,
        garage_address=f"{garage.city}, {garage.street}",
        transactions=statement_items
    )
    template = env.get_template('driver.html')
    return template.render(**statement.dict())
