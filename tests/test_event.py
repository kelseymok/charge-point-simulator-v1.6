from event import Event


class TestEvent:
    def test_format(self):
        e = Event(
            charge_point_id="123",
            action="Heartbeat",
            body={},
            write_timestamp="2023-01-01T09:00:00+00:00"
        )
        result = e.format()
        assert result == {
            "action": "Heartbeat",
            "body": "{}",
            "charge_point_id": "123",
            "write_timestamp": "2023-01-01T09:00:00+00:00",
        }

