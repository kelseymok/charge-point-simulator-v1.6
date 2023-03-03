from typing import List

from event import Event


class EventCollector:
    def __init__(self):
        self.events = []

    def add_events(self, events: List[Event]):
        # print(f"Adding events {events}")
        self.events = self.events + events

    def get_events(self):
        return [(e.__dict__) for item in self.events for e in (item if isinstance(item, list) else [item])]

