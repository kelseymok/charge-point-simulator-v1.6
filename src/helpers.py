from dateutil import parser
from freezegun import freeze_time
from datetime import datetime, timezone, timedelta
from typing import Callable, List


def pulse(f_request: Callable, f_response: Callable, starting_time: str, ending_time: str, freq=60 * 5,  **kwargs):
    collect_requests = []
    collect_responses = []
    with freeze_time(starting_time) as frozen_datetime:
        while (now := datetime.now(timezone.utc)) < parser.parse(ending_time):
            request = f_request(**kwargs, timestamp=now.isoformat())
            collect_requests.append((request, now.isoformat()))
            response_time = now + timedelta(seconds=1)
            response = f_response(**kwargs, now=response_time)
            collect_responses.append((response, response_time.isoformat()))
            frozen_datetime.tick(freq)

    return collect_requests, collect_responses


def flatten_list_of_lists(l: List):
    return [item for sublist in l for item in sublist]