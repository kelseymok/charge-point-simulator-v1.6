import asyncio
from datetime import datetime, timezone

import pandas as pd

from meter import Meter
from src.charge_point import ChargePoint
from event_collector import EventCollector
from transactions import Transactions
from config import charge_point_config
from deltalake.writer import write_deltalake

transactions_storage = Transactions()


def write_events(events):
    now = int(datetime.now(timezone.utc).timestamp())
    df = pd.DataFrame.from_records(events)
    df["write_timestamp_epoch"] = pd.to_datetime(df["write_timestamp"])
    df.sort_values(by="write_timestamp_epoch", inplace=True)
    df.to_json(f"../out/{now}.json", orient="records")
    df.to_csv(f"../out/{now}.csv", index=False, escapechar="\\", doublequote=False)
    df.to_parquet(f"../out/{now}.parquet")
    write_deltalake(f'../out/{now}/delta', df, partition_by=["action", "message_type", "charge_point_id"], mode='append')


async def main():
    event_collector = EventCollector()
    charge_points = [
        ChargePoint(meter=Meter(), transactions_storage=transactions_storage, event_collector=event_collector, config=i)
        for i in charge_point_config()
    ]

    for cp in charge_points:
        await cp.start()

    event_collector.add_events(transactions_storage.play_transactions())
    write_events(event_collector.get_events())

if __name__ == "__main__":
    asyncio.run(main())




