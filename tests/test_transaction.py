import random

from event import Event
from transaction import Transaction


class TestTransaction:

    def test_increase_meter(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        t._increase_meter(power_import=1000)
        assert t.meter_current == 1000
        t._increase_meter(power_import=1050)
        assert t.meter_current == 2050

    def test_start(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:10:00+00:00"
        )
        result = t.start()
        assert t.meter_current > 0
        assert len(result) == 4
        assert [x.action for x in result] == ["StartTransaction", "MeterValues", "MeterValues", "StopTransaction"]

    def test__start(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._start()
        assert result.__dict__ == Event(
            charge_point_id="123",
            action="StartTransaction",
            body={
                "connector_id": 1,
                "id_tag": "201e331c-a315-45d7-b43a-e2bc931b9981",
                "meter_start": 0,
                "timestamp": "2022-01-01T08:00:00+00:00",
                "reservation_id": None
            },
            write_timestamp="2022-01-01T08:00:00+00:00"
        ).__dict__

    def test__stop(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._stop()
        assert result.__dict__ == Event(
            charge_point_id="123",
            action="StopTransaction",
            body={
                "meter_stop": 0,
                "timestamp": "2022-01-01T09:00:00+00:00",
                "transaction_id": 1,
                "reason": None,
                "id_tag": "201e331c-a315-45d7-b43a-e2bc931b9981",
                "transaction_data": None
            },
            write_timestamp="2022-01-01T09:00:00+00:00"
        ).__dict__

    def test__meter_values_pulse(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._meter_values_pulse()
        assert len(result) == 3
        assert [x.action for x in result] == ["MeterValues", "MeterValues", "MeterValues"]

    def test__start_transaction(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._start_transaction()
        assert result == {
            "connector_id": 1,
            "id_tag": "201e331c-a315-45d7-b43a-e2bc931b9981",
            "meter_start": 0,
            "reservation_id": None,
            "timestamp": "2022-01-01T08:00:00+00:00"
        }

    def test__stop_transaction(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._stop_transaction()
        assert result == {
            "id_tag": "201e331c-a315-45d7-b43a-e2bc931b9981",
            "meter_stop": 0,
            "reason": None,
            "timestamp": "2022-01-01T08:15:00+00:00",
            "transaction_data": None,
            "transaction_id": 1
        }

    def test__add_noise(self):
        random.seed(10)
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._add_noise(3, 10)
        assert result == 10.43

    def test__meter_values(self):
        random.seed(10)
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
        )
        result = t._meter_values(power_import=1000, connector_id=1, transaction_id=1, timestamp="2023-01-01T08:00:00+00:00")
        assert result == {
            "connector_id": 1,
            "meter_value": [
                {
                    "sampled_value": [
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Voltage",
                        "phase": "L1-N",
                        "unit": "V",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Current.Import",
                        "phase": "L1",
                        "unit": "A",
                        "value": "5.72"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Power.Active.Import",
                        "phase": "L1",
                        "unit": "W",
                        "value": "1002.86"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Voltage",
                        "phase": "L2-N",
                        "unit": "V",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Current.Import",
                        "phase": "L2",
                        "unit": "A",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Power.Active.Import",
                        "phase": "L2",
                        "unit": "W",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Voltage",
                        "phase": "L3-N",
                        "unit": "V",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Current.Import",
                        "phase": "L3",
                        "unit": "A",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Power.Active.Import",
                        "phase": "L3",
                        "unit": "W",
                        "value": "0.0"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Energy.Active.Import.Register",
                        "phase": None,
                        "unit": "Wh",
                        "value": "1002.86"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Current.Import",
                        "phase": None,
                        "unit": "A",
                        "value": "5.72"
                    },
                    {
                        "context": "Sample.Periodic",
                        "format": "Raw",
                        "location": None,
                        "measurand": "Power.Active.Import",
                        "phase": None,
                        "unit": "W",
                        "value": "1002.86"
                    }
                ],
                "timestamp": "2023-01-01T08:00:00+00:00"
            }
        ],
        "transaction_id": 1
    }