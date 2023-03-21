import random

from event import MessageType
from meter import Meter
from transaction import Transaction
from generator_config import TransactionSessionConfig

class TestTransaction:

    def test_increase_meter(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
            meter=Meter(),
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T09:00:00+00:00",
                )
            ]
        )
        t._increase_meter(power_import=1000)
        assert t.meter.current_meter == 1000

        t._increase_meter(power_import=1050.234)
        assert t.meter.current_meter == 2050

    def test_start(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:10:00+00:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:10:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t.start()
        assert t.meter.current_meter > 0
        assert len(result) == 16
        assert [(x.message_type, x.action, x.write_timestamp) for x in result] == [
            (MessageType.request, "StartTransaction", "2022-01-01T08:00:01+00:00"),
            (MessageType.successful_response, "StartTransaction", "2022-01-01T08:00:02+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:00:03+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:00:04+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:00:04+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:00:05+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:00:06+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:05:06+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:00:07+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:05:07+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:10:00+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:10:01+00:00"),
            (MessageType.request, "StopTransaction", "2022-01-01T08:10:00+00:00"),
            (MessageType.successful_response, "StopTransaction", "2022-01-01T08:10:01+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:10:02+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:10:03+00:00")
        ]

    def test__start(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T09:00:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t._start()
        assert len(result) == 4
        assert [(x.message_type, x.action, x.write_timestamp) for x in result] == [
            (MessageType.request, "StartTransaction", "2022-01-01T08:00:01+00:00"),
            (MessageType.successful_response, "StartTransaction", "2022-01-01T08:00:02+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:00:03+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:00:04+00:00")
        ]

    def test__stop(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T09:00:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t._stop()
        assert [(x.message_type, x.action, x.write_timestamp) for x in result] == [
            (MessageType.request, "StopTransaction", "2022-01-01T09:00:00+00:00"),
            (MessageType.successful_response, "StopTransaction", "2022-01-01T09:00:01+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T09:00:02+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T09:00:03+00:00")
        ]

    def test__meter_values_pulse(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:15:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t._meter_values_pulse()
        assert len(result) == 10
        assert [(x.message_type, x.action) for x in result] == [
            (MessageType.request, "StatusNotification"),
            (MessageType.successful_response, "StatusNotification"),
            (MessageType.request, "MeterValues"),
            (MessageType.request, "MeterValues"),
            (MessageType.request, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.request, "StatusNotification"),
            (MessageType.successful_response, "StatusNotification")
        ]

    def test__meter_values_pulse_multiple_sessions(self):
        random.seed(10)
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T09:00:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:15:00+00:00",
                ),
                TransactionSessionConfig(
                    start_time="2022-01-01T08:45:00+00:00",
                    stop_time="2022-01-01T09:00:00+00:00",
                ),
            ],
            meter=Meter()
        )
        result = t._meter_values_pulse()
        assert len(result) == 20
        assert [(x.message_type, x.action, x.write_timestamp) for x in result] == [
            (MessageType.request, "StatusNotification", "2022-01-01T08:00:04+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:00:05+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:00:06+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:05:06+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:10:06+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:00:07+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:05:07+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:10:07+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:15:00+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:15:01+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T08:45:04+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T08:45:05+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:45:06+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:50:06+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:55:06+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:45:07+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:50:07+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:55:07+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T09:00:00+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T09:00:01+00:00")
        ]

    def test__start_transaction(self):
        t = Transaction(
            id=1,
            connector=1,
            charge_point_id="123",
            start_time="2022-01-01T08:00:00+00:00",
            stop_time="2022-01-01T08:15:00+00:00",
            id_tag="201e331c-a315-45d7-b43a-e2bc931b9981",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:15:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t._start_transaction_request()
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
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:15:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t._stop_transaction_request()
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
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:15:00+00:00",
                )
            ],
            meter=Meter()
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
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:15:00+00:00",
                )
            ],
            meter=Meter()
        )
        result = t._meter_values_request(power_import=1000, connector_id=1, transaction_id=1, timestamp="2023-01-01T08:00:00+00:00")
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

