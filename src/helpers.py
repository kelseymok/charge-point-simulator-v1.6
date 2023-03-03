from dateutil import parser
from freezegun import freeze_time
from datetime import datetime, timezone
from typing import Callable, List


def pulse(f: Callable, starting_time: str, ending_time: str, freq=60 * 5,  **kwargs):
    collect = []
    with freeze_time(starting_time) as frozen_datetime:
        while (now := datetime.now(timezone.utc)) < parser.parse(ending_time):
            result = f(**kwargs, timestamp=now.isoformat())
            collect.append((result, now.isoformat()))
            frozen_datetime.tick(freq)

    return collect


def flatten_list_of_lists(l: List):
    return [item for sublist in l for item in sublist]