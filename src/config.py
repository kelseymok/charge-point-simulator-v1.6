import uuid
import random
from datetime import datetime, timezone, timedelta
from dateutil import parser

from generator_config import ChargePointConfiguration, ChargePointTransactionConfig, TransactionSessionConfig

vendor = "ChargeAwesome LLC"


def on_time():
    return datetime(2023, 1, 1, 8, random.randint(0, 59), random.randint(0, 59), random.randint(0, 59), tzinfo=timezone.utc)


def off_time():
    return datetime(2023, 1, 6, 23, random.randint(0, 59), random.randint(0, 59), random.randint(0, 59), tzinfo=timezone.utc)


def add_hour_variation(a: datetime):
    variation = random.uniform(2, 12) * timedelta(hours=1)
    return a + variation


def build_transactions(on: str, off: str):
    current_date = parser.parse(on)
    off_date = parser.parse(off)
    transactions = []
    while current_date < off_date:
        local_start = add_hour_variation(current_date)
        current_date = local_start
        local_end = add_hour_variation(current_date)
        current_date = local_end
        if local_end < off_date:
            transactions.append(ChargePointTransactionConfig(
                connector=random.randint(1, 3),
                start_time=local_start.isoformat(),
                stop_time=local_end.isoformat(),
                sessions=build_sessions(local_start, local_end)
            ))

    return transactions


def add_minute_variation(a: datetime):
    variation = random.uniform(15, 60) * timedelta(minutes=1)
    return a + variation

def add_minute_variation_ceiling_aware(a: datetime, ceiling):
    variation = random.uniform(10, ceiling) * timedelta(minutes=1)
    return a + variation


def build_sessions(transaction_on: datetime, transaction_off: datetime):
    current_date = transaction_on
    sessions = []
    first_session = True

    while current_date < transaction_off:
        local_start = current_date if first_session else add_minute_variation(current_date)
        first_session = False
        current_date = local_start
        ceiling = round((transaction_off-local_start).seconds/60)
        local_end = add_minute_variation_ceiling_aware(current_date, ceiling)
        current_date = local_end
        if local_end < transaction_off:
            sessions.append(TransactionSessionConfig(
                start_time=local_start.isoformat(),
                stop_time=local_end.isoformat()
            ))

    return sessions


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
    return [ build_charge_point() for x in range(1) ]
