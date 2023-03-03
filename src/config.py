import uuid
import random
from datetime import datetime, timezone, timedelta
from dateutil import parser

from generator_config import ChargePointConfiguration, ChargePointTransactionConfig

vendor = "ChargeAwesome LLC"


def on_time():
    return datetime(2023, 1, 1, 8, random.randint(0, 59), random.randint(0, 59), random.randint(0, 59), tzinfo=timezone.utc)


def off_time():
    return datetime(2023, 1, 6, 23, random.randint(0, 59), random.randint(0, 59), random.randint(0, 59), tzinfo=timezone.utc)


def add_variation(a: datetime):
    variation = random.uniform(1, 10) * timedelta(hours=1)
    return a + variation


def build_transactions(on: str, off: str):
    current_date = parser.parse(on)
    transactions = []
    while current_date < parser.parse(off):
        local_start = add_variation(current_date)
        current_date = local_start
        local_end = add_variation(current_date)
        current_date = local_end

        transactions.append(ChargePointTransactionConfig(
            connector=random.randint(1, 3),
            start_time=local_start.isoformat(),
            stop_time=local_end.isoformat(),
        ))

    return transactions


def build_charge_point():
    on = on_time()
    off = off_time()
    c = ChargePointConfiguration(
        model=f"BB-{random.randint(0, 5)}",
        vendor=vendor,
        on_time=on.isoformat(),
        off_time=off.isoformat(),
        serial_number=str(uuid.uuid4()),
        transactions=build_transactions(on=on.isoformat(), off=off.isoformat())
    )
    return c


def charge_point_config():
    return [ build_charge_point() for x in range(10) ]
