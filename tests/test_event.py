import json

from event import Event, MessageType


class TestEvent:
    def test_format(self):
        e = Event(
            message_type=MessageType.request,
            charge_point_id="123",
            action="Heartbeat",
            body={},
            write_timestamp="2023-01-01T09:00:00+00:00"
        )
        result = e.format()
        assert result == {
            "message_type": MessageType.request,
            "action": "Heartbeat",
            "body": "{}",
            "charge_point_id": "123",
            "write_timestamp": "2023-01-01T09:00:00+00:00",
        }
        assert json.dumps(result) == '{"message_type": "2", "charge_point_id": "123", "action": "Heartbeat", "write_timestamp": "2023-01-01T09:00:00+00:00", "body": "{}"}'

