from event import Event, MessageType
from event_collector import EventCollector


class TestEventCollector:
    def test_add_event(self):
        collector = EventCollector()
        ocpp_event = Event(
            message_type=MessageType.request,
            charge_point_id="123",
            action="Heartbeat",
            body={},
            write_timestamp="2023-01-01T09:00:00+00:00"
        )
        collector.add_events([ocpp_event])
        assert collector.events == [ocpp_event]

    def test_get_events(self):
        collector = EventCollector()
        ocpp_event = Event(
            message_type=MessageType.request,
            charge_point_id="123",
            action="Heartbeat",
            body={},
            write_timestamp = "2023-01-01T09:00:00+00:00"
        )
        collector.add_events([ocpp_event])
        assert collector.get_events() == [{
            "message_type": MessageType.request,
            "action": "Heartbeat",
            "body": '{}',
            "charge_point_id": "123",
            "write_timestamp": "2023-01-01T09:00:00+00:00"
        }]