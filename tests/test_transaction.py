import random

from ocpp.v16.enums import AuthorizationStatus

from event import Event, MessageType
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
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T09:00:00+00:00",
                )
            ]
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
            stop_time="2022-01-01T08:10:00+00:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:00:00+00:00",
                    stop_time="2022-01-01T08:10:00+00:00",
                )
            ]
        )
        result = t.start()
        assert t.meter_current > 0
        assert len(result) == 8
        assert [(x.message_type, x.action) for x in result] == [
            (MessageType.request, "StartTransaction"),
            (MessageType.successful_response, "StartTransaction"),
            (MessageType.request,"MeterValues"),
            (MessageType.request,"MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.request, "StopTransaction"),
            (MessageType.successful_response, "StopTransaction"),
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
            ]
        )
        result = t._start()
        assert len(result) == 2
        assert result[0].__dict__ == Event(
            message_type=MessageType.request,
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
        assert result[1].__dict__ == Event(
            message_type=MessageType.successful_response,
            charge_point_id="123",
            action="StartTransaction",
            body={
                "transaction_id": 1,
                "id_tag_info": {
                    "status": AuthorizationStatus.accepted,
                    "parent_id_tag": "201e331c-a315-45d7-b43a-e2bc931b9981",
                    "expiry_date": None
                }
            },
            write_timestamp="2022-01-01T08:00:01+00:00"
        ).__dict__

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
            ]
        )
        result = t._stop()
        assert result[0].__dict__ == Event(
            message_type=MessageType.request,
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
        assert result[1].__dict__ == Event(
            message_type=MessageType.successful_response,
            charge_point_id="123",
            action="StopTransaction",
            body={
                "id_tag_info": {
                    "expiry_date": None,
                    "parent_id_tag": "201e331c-a315-45d7-b43a-e2bc931b9981",
                    "status": AuthorizationStatus.accepted
                }
            },
            write_timestamp="2022-01-01T09:00:01+00:00"
        ).__dict__

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
            ]
        )
        result = t._meter_values_pulse()
        assert len(result) == 6
        assert [(x.message_type, x.action) for x in result] == [
            (MessageType.request, "MeterValues"),
            (MessageType.request, "MeterValues"),
            (MessageType.request, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
            (MessageType.successful_response, "MeterValues"),
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
            ]
        )
        result = t._meter_values_pulse()
        assert len(result) == 12
        assert [(x.message_type, x.action, x.write_timestamp) for x in result] == [
            (MessageType.request, "MeterValues", "2022-01-01T08:01:00+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:06:00+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:11:00+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:01:01+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:06:01+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:11:01+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:46:00+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:51:00+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T08:56:00+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:46:01+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:51:01+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T08:56:01+00:00"),
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
            ]
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
            ]
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
            ]
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
            ]
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

